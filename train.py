import os
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "data" / "almaty_brt_dataset.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "brt_gb_model.pkl"

def generate_mock_data(samples=1000):
    np.random.seed(42)
    hour = np.random.randint(6, 23, samples)
    is_peak = np.where((hour >= 7) & (hour <= 9) | (hour >= 17) & (hour <= 19), 1, 0)
    weather = np.random.choice([0, 1, 2], samples, p=[0.7, 0.2, 0.1])
    isolated = np.random.choice([0, 1], samples, p=[0.3, 0.7])
    speed = np.random.uniform(15.0, 45.0, samples)
    conflict = np.random.uniform(0.1, 1.0, samples)

    delay = (is_peak * 4.0) + (weather * 3.0) - (isolated * 3.5) - (speed * 0.1) + (conflict * 5.0) + np.random.normal(0, 1, samples)
    delay = np.maximum(0, delay)

    df = pd.DataFrame({
        "hour": hour,
        "is_peak_hour": is_peak,
        "weather_condition": weather,
        "brt_lane_isolated": isolated,
        "avg_speed_kmh": speed,
        "conflict_risk_index": conflict,
        "delay_minutes": delay
    })
    return df

def train():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR = ROOT_DIR / "data"
    
    # Создаем папку data, если её нет
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists() or DATA_PATH.is_dir():
        df = generate_mock_data()
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["delay_minutes"])
    y = df["delay_minutes"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()