import json
import yaml
import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def train():
    config = load_config()

    Path(config['model']['reports_path']).parent.mkdir(parents=True, exist_ok=True)
    Path(config['model']['save_path']).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(config['data']['raw_path'])

    num_features = config['model']['features']['numeric']
    cat_features = config['model']['features']['categorical']
    target = config['model']['target']

    X = df[num_features + cat_features]
    y = df[target]

    split_idx = int(len(df) * (1 - config['training']['test_size']))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )

    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)

    model = HistGradientBoostingRegressor(
        max_iter=config['training']['max_iter'],
        learning_rate=config['training']['learning_rate'],
        random_state=config['training']['random_state']
    )

    model.fit(X_train_prep, y_train)

    preds = model.predict(X_test_prep)

    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = {
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4)
    }

    # Сохраняем отчет в metrics.json
    with open(config['model']['reports_path'], 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)

    # Сохраняем обученную модель
    joblib.dump({'preprocessor': preprocessor, 'model': model}, config['model']['save_path'])

    print(f"Metrics: {metrics}")
    print("Model and metrics successfully saved!")

if __name__ == "__main__":
    train()