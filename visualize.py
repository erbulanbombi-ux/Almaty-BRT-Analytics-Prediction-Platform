import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

df = pd.read_csv('data/almaty_brt_dataset.csv')
model = joblib.load('models/brt_gb_model.pkl')

feature_names = ['hour', 'is_peak_hour', 'weather_condition', 'brt_lane_isolated', 'avg_speed_kmh', 'conflict_risk_index']
importances = model.feature_importances_

plt.figure(figsize=(10, 5))
indices = np.argsort(importances)[::-1]
plt.bar([feature_names[i] for i in indices], importances[indices], color='#2b5c8f')
plt.title('Almaty BRT Delay Drivers (Feature Importance)')
plt.ylabel('Importance Weight')
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig('assets/feature_importance.png', dpi=300)
print("✅ Chart saved to assets/feature_importance.png")