import os
import numpy as np
import pandas as pd

os.makedirs('data', exist_ok=True)
np.random.seed(42)

n_samples = 2880
timestamps = pd.date_range(start='2026-08-01', periods=n_samples, freq='15min')

# Real segments of Almaty's first LRT line (Tole Bi St -> Abylai Khan Ave -> Momyshuly St).
# Each corridor has different elevation and typical conflict levels, so encode
# corridor_id as strings (not raw ints) so training and inference always agree
# on the same categories.
corridor_ids = np.random.choice(
    ['tole-bi-01', 'abylai-khan-01', 'momyshuly-01'], size=n_samples
)

# elevation now varies BY corridor instead of being one constant for every row
# (a constant column has zero variance and the model can never learn from it).
elevation_by_corridor = {
    'tole-bi-01': 2.3,
    'abylai-khan-01': 1.2,
    'momyshuly-01': 3.6,
}
elevation_slope_deg = (
    pd.Series(corridor_ids).map(elevation_by_corridor).to_numpy()
    + np.random.normal(0, 0.1, size=n_samples)
)

# weather_impact as strings too, for the same reason as corridor_id above.
weather_labels = np.random.choice(
    ['clear', 'rain', 'snow'], size=n_samples, p=[0.7, 0.2, 0.1]
)
weather_impact_numeric = pd.Series(weather_labels).map(
    {'clear': 0, 'rain': 1, 'snow': 2}
).to_numpy()

data = {
    'timestamp': timestamps,
    'corridor_id': corridor_ids,
    'elevation_slope_deg': elevation_slope_deg,
    'lane_isolation_score': np.random.uniform(0.6, 1.0, size=n_samples),
    'turning_conflicts': np.random.randint(1, 8, size=n_samples),
    'passenger_density': np.random.uniform(20, 100, size=n_samples),
    'weather_impact': weather_labels,  # string, matches what the API will send
}

df = pd.DataFrame(data)
df['hour'] = df['timestamp'].dt.hour
df['is_peak_hour'] = df['hour'].isin([8, 9, 18, 19]).astype(int)

base_delay = (
    4.0
    + df['is_peak_hour'] * 5.0
    + df['elevation_slope_deg'] * 0.6
    - df['lane_isolation_score'] * 4.5
    + df['turning_conflicts'] * 0.7
    + weather_impact_numeric * 2.5
    + np.random.normal(0, 1.0, size=n_samples)
)
df['delay_minutes'] = base_delay.clip(lower=0).round(2)
df['delay_lag_15m'] = df['delay_minutes'].shift(1).fillna(df['delay_minutes'].mean())
df['delay_lag_30m'] = df['delay_minutes'].shift(2).fillna(df['delay_minutes'].mean())

df.to_csv('data/lrt_data.csv', index=False)
print(f"Generated {len(df)} rows -> data/lrt_data.csv")
print(df[['corridor_id', 'weather_impact', 'elevation_slope_deg']].drop_duplicates('corridor_id'))