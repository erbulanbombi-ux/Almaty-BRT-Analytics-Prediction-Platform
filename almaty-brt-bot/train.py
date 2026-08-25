from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "data" / "data" / "almaty_brt_data.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

print(f"Loading dataset from {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

target_column = "delay_minutes"
if target_column not in df.columns:
    raise ValueError(f"Dataset must contain a '{target_column}' column")

X = df.drop(columns=[target_column])
y = df[target_column]
categorical_features = [
    column for column in X.columns
    if pd.api.types.is_string_dtype(X[column]) or isinstance(X[column].dtype, pd.CategoricalDtype)
]
numeric_features = [column for column in X.columns if column not in categorical_features]

preprocessor = ColumnTransformer([
    ("numeric", SimpleImputer(strategy="median"), numeric_features),
    ("categorical", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]), categorical_features),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Gradient Boosting Regressor with Grid Search...")
param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1], 'max_depth': [3, 5]}
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", GradientBoostingRegressor(random_state=42)),
])
grid_search = GridSearchCV(
    pipeline,
    {f"model__{key}": value for key, value in param_grid.items()},
    cv=3,
    scoring="neg_mean_absolute_error" if len(y_train) < 10 else "r2",
    n_jobs=-1,
)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

predictions = best_model.predict(X_test)
print("\n--- Model Evaluation ---")
print(f"Best Parameters : {grid_search.best_params_}")
print(f"MAE             : {mean_absolute_error(y_test, predictions):.3f} min")
print(f"MSE             : {mean_squared_error(y_test, predictions):.3f}")
print(f"R2 Score        : {r2_score(y_test, predictions) * 100:.2f}%")

joblib.dump(best_model, MODEL_DIR / "brt_gb_model.pkl")
print(f"Model saved to {MODEL_DIR / 'brt_gb_model.pkl'}")