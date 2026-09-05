import yaml
import joblib
import pandas as pd
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from route_planner import dijkstra, simulate

app = FastAPI(title="Almaty LRT Delay Prediction API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=400, content={
        "detail": str(exc.errors()[0]["msg"]),
        "error_code": "INVALID_INPUT",
    })

@app.exception_handler(Exception)
async def internal_error_handler(request, exc):
    return JSONResponse(status_code=500, content={
        "detail": "Internal server error",
        "error_code": "INTERNAL_ERROR",
    })

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

class BatchItem(FeaturesInput):
    corridor_id: str

class BatchRequest(BaseModel):
    predictions: list[BatchItem]

class SimulationInput(BaseModel):
    traffic: int
    passenger_demand: int
    frequency: int

class RouteInput(BaseModel):
    start: str
    end: str

@app.get("/")
def home():
    return {"status": "OK", "message": "LRT Delay Prediction API Active"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/simulate")
def run_simulation(data: SimulationInput):
    return simulate(data.traffic, data.passenger_demand, data.frequency)

@app.post("/route")
def find_route(data: RouteInput):
    return dijkstra(data.start, data.end)

@app.post("/predict")
def predict_delay(data: FeaturesInput):
    input_df = pd.DataFrame([data.model_dump()])
    prepared_data = preprocessor.transform(input_df)
    prediction = float(model.predict(prepared_data)[0])
    risk = "low" if prediction < 1 else "moderate" if prediction < 2.5 else "high"
    return {
        "predicted_delay_minutes": round(prediction, 2),
        "risk_level": risk,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.post("/batch-predict")
def batch_predict(req: BatchRequest):
    results = []
    for item in req.predictions:
        input_df = pd.DataFrame([item.model_dump()])
        prepared = preprocessor.transform(input_df)
        pred = float(model.predict(prepared)[0])
        results.append({"corridor_id": item.corridor_id, "predicted_delay_minutes": round(pred, 2)})
    return {"results": results, "processed_count": len(results)}