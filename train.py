import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train():
    os.makedirs('models', exist_ok=True)
    
    df = pd.read_csv('data/brt_data.csv')
    
    features = [
        'corridor_id', 'elevation_slope_deg', 'lane_isolation_score',
        'turning_conflicts', 'passenger_density', 'weather_impact',
        'is_peak_hour', 'delay_lag_15m', 'delay_lag_30m'
    ]
    
    X = df[features]
    y = df['delay_minutes']
    
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    model = XGBRegressor(n_estimators=150, learning_rate=0.05, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")
    
    joblib.dump(model, 'models/brt_model.joblib')

if __name__ == "__main__":
    train()