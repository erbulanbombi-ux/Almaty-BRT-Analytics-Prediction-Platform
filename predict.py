import argparse
from pathlib import Path

import joblib
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "models" / "brt_gb_model.pkl"


def predict_delay(features: dict[str, object], model_path: Path = MODEL_PATH) -> float:
    """Return the predicted delay in minutes for one BRT segment."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run 'python train.py' first."
        )

    model = joblib.load(model_path)
    df_features = pd.DataFrame([features])
    prediction = model.predict(df_features)[0]
    return max(0.0, float(prediction))


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict Almaty BRT delay")
    parser.add_argument("--hour", type=int, required=True)
    parser.add_argument("--is-peak-hour", type=int, choices=[0, 1], required=True)
    parser.add_argument("--weather-condition", type=int, choices=[0, 1, 2], required=True, help="0: Clear, 1: Rain, 2: Snow")
    parser.add_argument("--brt-lane-isolated", type=int, choices=[0, 1], required=True)
    parser.add_argument("--avg-speed-kmh", type=float, required=True)
    parser.add_argument("--conflict-risk-index", type=float, required=True)
    args = parser.parse_args()

    features = {
        "hour": args.hour,
        "is_peak_hour": args.is_peak_hour,
        "weather_condition": args.weather_condition,
        "brt_lane_isolated": args.brt_lane_isolated,
        "avg_speed_kmh": args.avg_speed_kmh,
        "conflict_risk_index": args.conflict_risk_index,
    }

    delay = predict_delay(features)
    print(f"\n⚡ Predicted delay for Almaty BRT segment: {delay:.2f} minutes")


if __name__ == "__main__":
    main()