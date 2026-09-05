import os
import numpy as np
import pandas as pd
import osmnx as ox

os.makedirs('data', exist_ok=True)
np.random.seed(42)

try:
    G = ox.graph_from_place('Almaty, Kazakhstan', network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G)
    avg_elevation_gain = 4.2
except Exception:
    avg_elevation_gain = 4.2

n_samples = 2880
timestamps = pd.date_range(start='2026-08-01', periods=n_samples, freq='15min')

data = {
    'timestamp': timestamps,
    'corridor_id': np.random.choice(['tole-bi-01', 'abylai-khan-01', 'momyshuly-01'], size=n_samples),
    'lane_isolation_score': np.random.uniform(0.6, 1.0, size=n_samples),
    'turning_conflicts': np.random.randint(1, 8, size=n_samples),
    'passenger_density': np.random.uniform(20, 100, size=n_samples),
    'weather_impact': np.random.choice(['clear', 'rain', 'snow'], size=n_samples, p=[0.7, 0.2, 0.1]),
}

df = pd.DataFrame(data)
elevation_map = {'tole-bi-01': 2.3, 'abylai-khan-01': 1.2, 'momyshuly-01': 3.6}
df['elevation_slope_deg'] = df['corridor_id'].map(elevation_map) + np.random.normal(0, 0.1, n_samples)
df['hour'] = df['timestamp'].dt.hour
df['is_peak_hour'] = df['hour'].isin([8, 9, 18, 19]).astype(int)

base_delay = (
    4.0 
    + df['is_peak_hour'] * 5.0 
    + df['elevation_slope_deg'] * 0.6
    - df['lane_isolation_score'] * 4.5 
    + df['turning_conflicts'] * 0.7 
    + df['weather_impact'].map({'clear': 0, 'rain': 1, 'snow': 2}) * 2.5
    + np.random.normal(0, 1.0, size=n_samples)
)

df['delay_minutes'] = base_delay.clip(lower=0).round(2)

df['delay_lag_15m'] = df['delay_minutes'].shift(1).fillna(df['delay_minutes'].mean())
df['delay_lag_30m'] = df['delay_minutes'].shift(2).fillna(df['delay_minutes'].mean())

df.to_csv('data/lrt_data.csv', index=False)