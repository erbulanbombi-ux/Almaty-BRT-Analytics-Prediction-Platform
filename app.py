import yaml
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Almaty LRT Delay Prediction API")

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

saved_objects = joblib.load(config['model']['save_path'])
preprocessor = saved_objects['preprocessor']
model = saved_objects['model']

class FeaturesInput(BaseModel):
    elevation_slope_deg: float
    lane_isolation_score: float
    turning_conflicts: int
    passenger_density: float
    delay_lag_15m: float
    delay_lag_30m: float
    corridor_id: str
    weather_impact: str
    is_peak_hour: int

@app.get("/")
def home():
    return {"status": "OK", "message": "LRT Delay Prediction API Active"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict_delay(data: FeaturesInput):
    input_df = pd.DataFrame([data.model_dump()])
    prepared_data = preprocessor.transform(input_df)
    prediction = model.predict(prepared_data)[0]
    return {
        "predicted_delay_minutes": round(float(prediction), 2)
    }