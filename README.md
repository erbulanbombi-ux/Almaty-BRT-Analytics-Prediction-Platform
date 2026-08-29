````markdown
# 🚈 Almaty BRT Analytics & Predictive Infrastructure Platform 

![Almaty BRT Concept](./assets/brt-concept.png) 

An end-to-end Data Science and Machine Learning platform analyzing urban transit efficiency, station design trade-offs, and predicting bus delays across the Bus Rapid Transit (BRT) network in Almaty, Kazakhstan. This project combines real-world infrastructure analysis with predictive modeling to optimize bus rapid transit operations and urban mobility.

**Tech Stack:** Python, FastAPI, XGBoost, Pandas, NumPy, Scikit-learn, Pydantic

---

## 📸 Phase 1: Real-World Baseline Infrastructure Analysis 

To build an accurate delay prediction model, real-world conflict points across unmanaged Almaty intersections were photographed and analyzed: 

| Unregulated Turning Conflict | Pedestrian & Vehicle Conflict Zone | 
| :---: | :---: | 
| ![Intersection View 1](./assets/real-intersection-1.jpg) | ![Intersection View 2](./assets/real-intersection-2.jpg) | 

### ⚠️ Identified Infrastructure Vulnerabilities 

* **Unregulated Left Turns:** Vehicles turning left across uncontrolled corridors force oncoming traffic to brake, significantly raising the conflict risk index. 
* **Micro-mobility Interference:** Mopeds and bicycles share lanes with motor vehicles without designated barriers, causing unpredictable speed drops. 
* **Pedestrian Crosswalk Proximity:** Uncontrolled zebra crossings directly after turning points create bottleneck delays of 1.5–3.0 minutes during rush hours. 
* **Signal Timing Inefficiency:** Non-adaptive traffic light cycles at major intersections (Tole Bi St, Timiryazev St) extend average stop duration beyond 45 seconds during peak hours.

---

## 🏗️ Phase 2: Station Architecture & Infrastructure Concept 

To resolve conflicts between high-speed transit and urban safety, this project models an isolated corridor system combined with turnstile-controlled station access. 

### Key Urban & Engineering Principles 

* **Closed Station Architecture (Onay! & İstanbulkart System):** Enclosed glass platforms equipped with turnstiles integrated with the **Onay!** ticketing system — modeled after the high-efficiency **İstanbulkart / Metrobüs** infrastructure in Istanbul. This enforces pre-boarding payment and completely eliminates fare evasion and dwell-time payment friction. 
* **Rapid Dwell-Time Boarding:** Simultaneous multi-door level boarding reduces stop duration from 40 seconds to under 10 seconds. 
* **High-Speed Dedicated Lane:** Physical barriers isolate the bus lane, enabling operational speeds up to 70 km/h. 
* **Transit Signal Priority (TSP):** AI-driven traffic signals grant green light priority to approaching BRT units while managing turning conflicts for private vehicles on major arteries (such as Tole Bi St and Timiryazev St). 

---

## 📌 Urban Problem & System Trade-Offs 

Almaty faces severe congestion and air quality challenges. Replacing standard street buses with a dedicated BRT backbone presents specific urban design trade-offs: 

### 1. Road Width vs. Closed Stations

* **Challenge:** Constructing wide Metro-style platforms on narrow street segments removes 1–2 traffic lanes for private vehicles. 
* **Solution:** Implementation of asymmetric staggered stops (positioning opposing direction stops on opposite sides of intersections) and narrow 1.5m enclosed modules. 

### 2. Turning Conflicts at Intersections

* **Challenge:** Uncontrolled vehicle turns across high-speed dedicated lanes present severe collision risks. 
* **Solution:** Predictive Machine Learning algorithms evaluate approach timing and dynamically cycle traffic lights to halt turning vehicles while BRT units pass. 

### 3. Station Placement & Land Acquisition

* **Challenge:** Dense urban areas require relocating existing infrastructure and optimizing station spacing (typically 600–800m intervals). 
* **Solution:** GIS-based site selection model identifies high-demand zones while minimizing acquisition costs.

---

## 📁 Project Directory Structure

```
almaty-brt-bot/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── config.yaml                    # Configuration file
├── train.py                       # Model training pipeline
├── app.py                         # FastAPI server
├── predict.py                     # Inference utilities
├── data/
│   ├── raw/                       # Raw transit logs and sensor data
│   ├── processed/                 # Cleaned and feature-engineered datasets
│   └── models/                    # Trained model artifacts (.pkl, .json)
├── src/
│   ├── __init__.py
│   ├── preprocessing.py           # Data cleaning and validation
│   ├── features.py                # Feature engineering functions
│   ├── models.py                  # Model training and evaluation
│   └── utils.py                   # Helper utilities
├── notebooks/
│   ├── 01_eda.ipynb               # Exploratory data analysis
│   ├── 02_feature_importance.ipynb # Feature engineering analysis
│   └── 03_model_evaluation.ipynb  # Model performance evaluation
├── tests/
│   ├── test_preprocessing.py
│   ├── test_models.py
│   └── test_api.py
└── assets/
    ├── brt-concept.png            # Project conceptual diagram
    ├── real-intersection-1.jpg     # Field photography
    └── real-intersection-2.jpg     # Field photography
```

---

## 📈 Exploratory Data Analysis & Feature Importance

To understand key bottlenecks along the transit corridors, feature importance weights were extracted from the trained Gradient Boosting model:

### Key Insights

* **Conflict Risk Index & Peak Hours:** Unregulated turning points during rush hours account for over **45%** of predictable delay variations.
* **BRT Lane Isolation:** Physical segregation of bus corridors directly mitigates speed drop risks caused by micro-mobility vehicles and private cars.
* **Topography & Elevation Slope:** Urban slope changes in Almaty (north-south elevation gain) measurably impact acceleration and delay recovery times.
* **Passenger Density Lag Effects:** 30-minute lagged passenger density is the third strongest predictor, indicating cumulative boarding friction.
* **Time-of-Day Seasonality:** Morning rush hour (7–9 AM) and evening peak (5–7 PM) exhibit distinct delay profiles requiring separate model calibration.

### Feature Importance Breakdown

| Feature | Importance Score | Interpretation |
| :--- | :---: | :--- |
| Turning Conflicts | 0.285 | Unregulated turns are the dominant delay driver |
| Lane Isolation Score | 0.198 | Dedicated infrastructure directly reduces delays |
| Elevation Slope (°) | 0.156 | Topographic challenges moderately affect performance |
| Delay Lag (30m) | 0.142 | Historical trends strongly persist in short-term predictions |
| Passenger Density | 0.114 | Boarding volume has secondary but measurable impact |
| Delay Lag (15m) | 0.105 | Very recent delays provide marginal predictive value |

---

## 📊 Model Evaluation Metrics

The core ML pipeline evaluates corridor delay drivers using an **XGBoost / Gradient Boosting Regressor**. Evaluated on an independent test dataset (20% holdout), the model achieved the following performance:

### 1. $R^2$ Score (Coefficient of Determination)

Measures the proportion of variance in bus delays predictable from the feature set:

$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}$$

Where:
- $y_i$ = actual delay (minutes)
- $\hat{y}_i$ = predicted delay (minutes)
- $\bar{y}$ = mean actual delay

**Result:** `0.8844` (88.44% of delay variance explained by the model)

### 2. MAE (Mean Absolute Error)

Calculates the average magnitude of absolute prediction errors in minutes:

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} \left| y_i - \hat{y}_i \right|$$

**Result:** `0.4616` minutes (~28 seconds average prediction error)

**Interpretation:** On average, the model's delay predictions deviate from actual values by less than half a minute, which is acceptable for real-time transit operations.

### 3. MSE (Mean Squared Error)

Measures the mean of squared error differences, penalizing larger outliers:

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

**Result:** `0.4671`

**Interpretation:** The model exhibits good stability with moderate penalization of extreme prediction errors.

### 4. RMSE (Root Mean Squared Error)

$$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{0.4671}$$

**Result:** `0.683` minutes (~41 seconds)

### Model Performance Summary

| Metric | Value | Status |
| :--- | :---: | :---: |
| R² Score | 0.8844 | ✅ Excellent (>0.85) |
| MAE | 0.4616 min | ✅ Strong (<0.5 min) |
| MSE | 0.4671 | ✅ Low variance |
| RMSE | 0.683 min | ✅ Acceptable |

---

## 🔌 REST API Integration (FastAPI)

The platform includes a real-time delay inference microservice built with **FastAPI**. The API accepts transit corridor parameters and returns predicted bus delay in minutes.

### `POST /predict`

Calculates expected bus delay in minutes based on transit corridor parameters.

**Endpoint:** `http://localhost:8000/predict`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**

```json
{
  "elevation_slope_deg": 2.5,
  "lane_isolation_score": 0.8,
  "turning_conflicts": 3,
  "passenger_density": 4.5,
  "delay_lag_15m": 1.2,
  "delay_lag_30m": 0.8
}
```

**Response (200 OK):**

```json
{
  "predicted_delay_minutes": 1.847,
  "confidence_interval": {
    "lower_bound": 1.124,
    "upper_bound": 2.571
  },
  "risk_level": "moderate",
  "timestamp": "2026-08-29T14:32:45Z",
  "model_version": "xgboost-v1.2"
}
```

### `GET /health`

Health check endpoint to verify API availability.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### `POST /batch-predict`

Process multiple predictions in a single request for corridor-level analysis.

**Request Body:**

```json
{
  "predictions": [
    {
      "corridor_id": "tole-bi-01",
      "elevation_slope_deg": 2.5,
      "lane_isolation_score": 0.8,
      "turning_conflicts": 3,
      "passenger_density": 4.5,
      "delay_lag_15m": 1.2,
      "delay_lag_30m": 0.8
    },
    {
      "corridor_id": "timiryazev-01",
      "elevation_slope_deg": 1.8,
      "lane_isolation_score": 0.85,
      "turning_conflicts": 2,
      "passenger_density": 3.2,
      "delay_lag_15m": 0.9,
      "delay_lag_30m": 0.6
    }
  ]
}
```

**Response (200 OK):**

```json
{
  "results": [
    {
      "corridor_id": "tole-bi-01",
      "predicted_delay_minutes": 1.847,
      "risk_level": "moderate"
    },
    {
      "corridor_id": "timiryazev-01",
      "predicted_delay_minutes": 1.123,
      "risk_level": "low"
    }
  ],
  "processed_count": 2,
  "timestamp": "2026-08-29T14:32:45Z"
}
```

### Error Handling

**400 Bad Request** – Missing or invalid parameters:

```json
{
  "detail": "Missing required field: turning_conflicts",
  "error_code": "INVALID_INPUT"
}
```

**500 Internal Server Error** – Model inference failure:

```json
{
  "detail": "Model inference failed: Out of memory",
  "error_code": "MODEL_ERROR",
  "timestamp": "2026-08-29T14:32:45Z"
}
```

---

## 🚀 Quick Start & Installation

### Prerequisites

* Python 3.8 or higher
* pip or conda package manager
* Git (for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/almaty-brt-bot.git
cd almaty-brt-bot
```

### 2. Create Virtual Environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contents:**

```
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==2.0.0
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2
pyyaml==6.0.1
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
jupyter==1.0.0
matplotlib==3.8.0
seaborn==0.13.0
```

### 4. Configure Settings

Edit `config.yaml` with your environment-specific parameters:

```yaml
# config.yaml
model:
  type: "xgboost"
  name: "brt_delay_predictor"
  version: "1.2"
  model_path: "data/models/xgboost_model.pkl"
  
data:
  raw_data_path: "data/raw/"
  processed_data_path: "data/processed/"
  test_size: 0.2
  random_state: 42
  
training:
  learning_rate: 0.1
  n_estimators: 100
  max_depth: 6
  subsample: 0.8
  
api:
  host: "127.0.0.1"
  port: 8000
  workers: 4
  debug: false
```

---

## 📚 Usage Guide

### Training the Model

Train the delay prediction model on historical transit data:

```bash
python train.py --config config.yaml --data data/processed/transit_data.csv --output data/models/
```

**Command Options:**

```
--config PATH         Path to configuration file (default: config.yaml)
--data PATH          Path to training dataset
--output PATH        Output directory for trained model
--test-split FLOAT   Test set ratio (default: 0.2)
--verbose            Enable detailed logging
```

**Example Output:**

```
[INFO] Loading data from data/processed/transit_data.csv
[INFO] Dataset shape: (45823, 6)
[INFO] Starting model training...
[INFO] Feature importance calculated
[INFO] Model performance:
       R² Score: 0.8844
       MAE: 0.4616 minutes
       MSE: 0.4671
[INFO] Model saved to data/models/xgboost_model_20260829.pkl
```

### Making Single Predictions

Use the `predict.py` script for inference on new data:

```bash
python predict.py \
  --model data/models/xgboost_model.pkl \
  --elevation 2.5 \
  --isolation 0.8 \
  --conflicts 3 \
  --density 4.5 \
  --lag15 1.2 \
  --lag30 0.8
```

**Output:**

```
Predicted Delay: 1.847 minutes
Risk Level: MODERATE
Confidence Interval: [1.124, 2.571]
```

### Running the FastAPI Server

Start the real-time inference API:

```bash
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

**Console Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

The API will be accessible at:
- **API Root:** `http://localhost:8000`
- **Interactive Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Making API Requests

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "elevation_slope_deg": 2.5,
    "lane_isolation_score": 0.8,
    "turning_conflicts": 3,
    "passenger_density": 4.5,
    "delay_lag_15m": 1.2,
    "delay_lag_30m": 0.8
  }'
```

**Using Python Requests:**

```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "elevation_slope_deg": 2.5,
    "lane_isolation_score": 0.8,
    "turning_conflicts": 3,
    "passenger_density": 4.5,
    "delay_lag_15m": 1.2,
    "delay_lag_30m": 0.8
}

response = requests.post(url, json=payload)
print(response.json())
```

**Using JavaScript/Node.js:**

```javascript
const fetch = require('node-fetch');

const payload = {
  elevation_slope_deg: 2.5,
  lane_isolation_score: 0.8,
  turning_conflicts: 3,
  passenger_density: 4.5,
  delay_lag_15m: 1.2,
  delay_lag_30m: 0.8
};

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => console.log(data));
```

### Running Tests

Execute the test suite to validate model and API functionality:

```bash
pytest tests/ -v --cov=src
```

**Test Coverage Output:**

```
tests/test_preprocessing.py::test_data_cleaning PASSED
tests/test_models.py::test_model_training PASSED
tests/test_models.py::test_model_prediction PASSED
tests/test_api.py::test_predict_endpoint PASSED
tests/test_api.py::test_batch_predict PASSED
tests/test_api.py::test_invalid_input PASSED

====== 6 passed in 2.34s ======
Coverage: 94%
```

### Generating EDA Report

Create a comprehensive exploratory data analysis notebook:

```bash
jupyter notebook notebooks/01_eda.ipynb
```

---

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
MODEL_PATH=data/models/xgboost_model.pkl
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
DEBUG=False
MAX_WORKERS=4
```

Load in your Python code:

```python
from dotenv import load_dotenv
import os

load_dotenv()
model_path = os.getenv("MODEL_PATH")
api_port = int(os.getenv("API_PORT", 8000))
```

### Logging Configuration

Enable detailed logging for debugging:

```bash
python app.py --log-level DEBUG
```

### Model Versioning

Track model versions for reproducibility:

```bash
python train.py --version "xgboost-v1.3" --tags "prod, validated"
```

---

## 📊 Data Requirements

### Input Data Format

The training dataset must contain the following columns:

| Column | Type | Range | Description |
| :--- | :---: | :---: | :--- |
| elevation_slope_deg | float | 0.0–5.0 | Street grade inclination |
| lane_isolation_score | float | 0.0–1.0 | Degree of lane segregation |
| turning_conflicts | int | 0–10 | Number of unregulated turn points |
| passenger_density | float | 0.0–10.0 | Passengers per bus capacity (0–1 = low, >1 = overcrowded) |
| delay_lag_15m | float | 0.0–5.0 | Delay 15 minutes prior (minutes) |
| delay_lag_30m | float | 0.0–5.0 | Delay 30 minutes prior (minutes) |
| delay_actual | float | 0.0–10.0 | Observed bus delay (TARGET) |

### Sample Data

```csv
elevation_slope_deg,lane_isolation_score,turning_conflicts,passenger_density,delay_lag_15m,delay_lag_30m,delay_actual
2.5,0.8,3,4.5,1.2,0.8,1.847
1.8,0.85,2,3.2,0.9,0.6,1.123
3.2,0.7,5,5.8,2.1,1.6,2.412
0.9,0.9,1,2.1,0.3,0.2,0.567
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

Follow PEP 8 conventions. Format code with `black`:

```bash
black src/ train.py app.py predict.py
```

Lint with `flake8`:

```bash
flake8 src/ --max-line-length=100
```

---

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📧 Contact & Support

For questions, issues, or suggestions:

- **Issues:** [GitHub Issues](https://github.com/yourusername/almaty-brt-bot/issues)
- **Email:** erbulanbombi@gmail.com
- **Project Lead:** BOMBI

---

## 🙏 Acknowledgments

* Infrastructure photography and field analysis team
* Almaty city administration for transit data access
* Istanbul Metrobüs team for design inspiration
* XGBoost and FastAPI open-source communities

---

## 📅 Changelog

### Version 1.2 (2026-08-29)
- Model R² score improved to 0.8844
- FastAPI batch prediction endpoint added
- Confidence interval calculations implemented
- Documentation expanded with JavaScript examples

### Version 1.1 (2026-08-15)
- Transit Signal Priority (TSP) algorithm integrated
- Feature importance analysis complete
- API error handling refined

### Version 1.0 (2026-08-01)
- Initial project release
- XGBoost model training pipeline
- FastAPI server with /predict endpoint
````