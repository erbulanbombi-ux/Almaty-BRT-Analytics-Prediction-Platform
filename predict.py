import argparse
import joblib
import pandas as pd

def predict():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corridor_id', type=int, default=1)
    parser.add_argument('--slope', type=float, default=4.2)
    parser.add_argument('--lane_isolation', type=float, default=0.8)
    parser.add_argument('--conflicts', type=int, default=3)
    parser.add_argument('--passengers', type=float, default=65.0)
    parser.add_argument('--weather', type=int, default=0)
    parser.add_argument('--is_peak', type=int, default=1)
    parser.add_argument('--prev_delay', type=float, default=8.5)

    args = parser.parse_args()
    model = joblib.load('models/brt_model.joblib')

    input_df = pd.DataFrame([{
        'corridor_id': args.corridor_id,
        'elevation_slope_deg': args.slope,
        'lane_isolation_score': args.lane_isolation,
        'turning_conflicts': args.conflicts,
        'passenger_density': args.passengers,
        'weather_impact': args.weather,
        'is_peak_hour': args.is_peak,
        'delay_lag_15m': args.prev_delay,
        'delay_lag_30m': args.prev_delay * 0.9
    }])

    prediction = model.predict(input_df)[0]
    print(f"Predicted delay: {prediction:.2f} minutes")

if __name__ == "__main__":
    predict()