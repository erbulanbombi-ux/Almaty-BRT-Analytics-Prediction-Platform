import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def plot_analytics():
    df = pd.read_csv('data/brt_data.csv')
    model = joblib.load('models/brt_model.joblib')
    
    features = [
        'corridor_id', 'elevation_slope_deg', 'lane_isolation_score',
        'turning_conflicts', 'passenger_density', 'weather_impact',
        'is_peak_hour', 'delay_lag_15m', 'delay_lag_30m'
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    importances = model.feature_importances_
    feat_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values('Importance', ascending=False)
    
    sns.barplot(data=feat_df, x='Importance', y='Feature', ax=axes[0], palette='viridis')
    axes[0].set_title('Feature Importance')
    
    sns.scatterplot(data=df, x='lane_isolation_score', y='delay_minutes', hue='is_peak_hour', alpha=0.6, ax=axes[1])
    axes[1].set_title('Delay vs Lane Isolation')
    
    plt.tight_layout()
    plt.savefig('brt_analytics.png')
    plt.show()

if __name__ == "__main__":
    plot_analytics()