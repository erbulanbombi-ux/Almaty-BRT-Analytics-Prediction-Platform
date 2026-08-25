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
	prediction = model.predict(pd.DataFrame([features]))[0]
	return max(0.0, float(prediction))


def main() -> None:
	parser = argparse.ArgumentParser(description="Predict Almaty BRT delay")
	parser.add_argument("--hour", type=int, required=True)
	parser.add_argument("--is-peak-hour", type=int, choices=[0, 1], required=True)
	parser.add_argument("--weather-condition", required=True)
	parser.add_argument("--brt-lane-isolated", type=int, choices=[0, 1], required=True)
	parser.add_argument("--avg-speed-kmh", type=float, required=True)
	parser.add_argument("--conflict-risk-index", type=float, required=True)
	args = parser.parse_args()

	features = vars(args).copy()
	features["is_peak_hour"] = features.pop("is_peak_hour")
	features["weather_condition"] = features.pop("weather_condition")
	features["brt_lane_isolated"] = features.pop("brt_lane_isolated")
	features["avg_speed_kmh"] = features.pop("avg_speed_kmh")
	features["conflict_risk_index"] = features.pop("conflict_risk_index")
	print(f"Predicted delay: {predict_delay(features):.2f} minutes")


if __name__ == "__main__":
	main()
