# 🚌 Almaty BRT Analytics & Predictive Infrastructure Platform

An end-to-end Data Science and Machine Learning project analyzing the urban transit transformation in Almaty, Kazakhstan. This repository models travel time optimization, collision risk reduction at turning points, fare evasion prevention, and traffic signal synchronization for high-speed Bus Rapid Transit (BRT) lines.

---

## 📸 Station Architecture & Infrastructure Concept

To solve the conflict between high-speed transit and urban safety, this project models an isolated corridor system combined with turnstile-controlled access.

![Almaty BRT Station Concept](assets/brt-concept.jpg)

### Key Urban & Engineering Principles:
* **Closed Station Architecture:** Enclosed glass platforms equipped with turnstiles (Onay integration, similar to the Istanbul Metrobüs / Metro system) enforce pre-boarding payment and minimize fare evasion.
* **Rapid Dwell-Time Boarding:** Simultaneous multi-door boarding level with the platform reduces stop duration from 40 seconds to under 10 seconds.
* **High-Speed Dedicated Lane:** Physical barriers isolate the bus lane, allowing speed limits up to 70 km/h.
* **Transit Signal Priority (TSP):** AI-driven traffic signals grant green light priority to approaching BRT units while managing turning conflicts for private vehicles on major arteries (such as Tole Bi St).

---

## 📌 Urban Problem & System Trade-Offs

Almaty faces severe congestion and air quality challenges. Replacing standard street buses with a dedicated BRT backbone presents specific urban design trade-offs:

1. **Road Width vs. Closed Stations:**
   * *Challenge:* Constructing wide Metro-style platforms on narrow street segments removes 1–2 traffic lanes for private vehicles.
   * *Solution:* Implementation of asymmetric staggered stops (positioning opposing direction stops on opposite sides of intersections) and narrow 1.5m enclosed modules.
2. **Turning Conflicts at Intersections:**
   * *Challenge:* Uncontrolled vehicle left/right turns across high-speed dedicated lanes present severe collision risks.
   * *Solution:* Predictive Machine Learning algorithms evaluate approach timing and dynamically cycle traffic lights to halt turning cars while BRT units pass.

---

## 🔬 Machine Learning Architecture

The core pipeline evaluates corridor efficiency and predicts travel delays using standard regression models (`GradientBoostingRegressor`, `RandomForestRegressor`).

### Model Features:
* `street_width`: Total road width in meters.
* `traffic_density`: Real-time traffic congestion score (0.0 to 1.0).
* `is_peak_hour`: Binary indicator for rush-hour windows.
* `station_type`: `0` for Open Stops, `1` for Closed Turnstile Platforms.
* `turn_conflict_points`: Count of unregulated turning driveways/intersections.
* `tsp_enabled`: Binary indicator for active Transit Signal Priority.
* **Target Variable (`delay_minutes`):** Predicted transit delay along the segment.

---

## 🛠️ Project Structure

```text
almaty-brt-bot/
├── assets/
│   └── brt-concept.jpg       # High-speed enclosed station visual concept
├── data/
│   └── almaty_brt_dataset.csv # Generated traffic dataset
├── models/
│   ├── brt_gb_model.pkl      # Trained Gradient Boosting binary
│   └── scaler.pkl            # StandardScaler artifact
├── train.py                  # ML pipeline, data generation & model training
├── requirements.txt          # Python dependencies
└── README.md                 # Master documentation