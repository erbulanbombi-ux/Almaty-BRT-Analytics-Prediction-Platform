import json
import yaml
import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_preprocessor(num_features, cat_features):
    return ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )

def build_model(config):
    return HistGradientBoostingRegressor(
        max_iter=config['training']['max_iter'],
        learning_rate=config['training']['learning_rate'],
        random_state=config['training']['random_state']
    )

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

    preprocessor = build_preprocessor(num_features, cat_features)

    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)

    model = build_model(config)

    model.fit(X_train_prep, y_train)

    preds = model.predict(X_test_prep)

    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    comparison = {'Ridge baseline': {}}
    baseline_preprocessor = build_preprocessor(num_features, cat_features)
    baseline_train = baseline_preprocessor.fit_transform(X_train)
    baseline_test = baseline_preprocessor.transform(X_test)
    baseline = Ridge(alpha=1.0).fit(baseline_train, y_train)
    baseline_preds = baseline.predict(baseline_test)
    comparison['Ridge baseline'] = {
        'MAE': round(float(mean_absolute_error(y_test, baseline_preds)), 4),
        'RMSE': round(float(root_mean_squared_error(y_test, baseline_preds)), 4),
        'R2': round(float(r2_score(y_test, baseline_preds)), 4),
    }
    comparison['HistGradientBoosting'] = {
        'MAE': round(float(mae), 4),
        'RMSE': round(float(rmse), 4),
        'R2': round(float(r2), 4),
    }

    time_split = TimeSeriesSplit(n_splits=5)
    cv_scores = []
    for train_indices, validation_indices in time_split.split(X):
        fold_preprocessor = build_preprocessor(num_features, cat_features)
        fold_train = fold_preprocessor.fit_transform(X.iloc[train_indices])
        fold_validation = fold_preprocessor.transform(X.iloc[validation_indices])
        fold_model = clone(build_model(config))
        fold_model.fit(fold_train, y.iloc[train_indices])
        fold_predictions = fold_model.predict(fold_validation)
        cv_scores.append({
            'MAE': round(float(mean_absolute_error(y.iloc[validation_indices], fold_predictions)), 4),
            'RMSE': round(float(root_mean_squared_error(y.iloc[validation_indices], fold_predictions)), 4),
            'R2': round(float(r2_score(y.iloc[validation_indices], fold_predictions)), 4),
        })

    metrics = {
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4),
        "time_series_cv": cv_scores,
        "model_comparison": comparison,
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