# Almaty LRT Simulation Lab

An interactive research prototype for exploring a future LRT network in Almaty. The main project flow is available on one page:

`LRT route -> stations -> predicted delay -> simulation result`

> The current data and calculations are synthetic. This project demonstrates an engineering and ML workflow and is not an official forecast for Almaty's transport system.

![CI](https://github.com/erbulanbombi-ux/Almaty-LRT-Analytics-Prediction-Platform/actions/workflows/ci.yml/badge.svg)

## What you can do

- choose departure and destination stations;
- find the shortest route through the LRT network with Dijkstra;
- change `traffic`, `passenger demand`, and `LRT frequency`;
- see how delay, travel time, and schedule reliability change;
- train a `HistGradientBoostingRegressor` on the demonstration dataset;
- compare the model with a Ridge baseline using `TimeSeriesSplit`;
- open the EDA notebook with distributions and correlations.

## Run the demo

Start a local static server:

```powershell
python -m http.server 5500
```

Open <http://localhost:5500>.

The page works without the Python API: route planning and simulation run in the browser. When the API is running, the ML prediction card also requests the `/predict` endpoint.

## Run the ML API

Create an environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Train the model and start the API:

```powershell
python train.py
uvicorn app:app --reload
```

Available endpoints:

- `GET /health` - model status;
- `POST /predict` - delay prediction from model features;
- `POST /simulate` - movement scenario calculation;
- `POST /route` - shortest route with Dijkstra.

Interactive API documentation is available at `/docs`. The README intentionally keeps API examples short.

## Model and data

`train.py` saves the model to `models/brt_model.joblib` and metrics to `reports/metrics.json`. The historical `brt_*` names remain for compatibility with the current files.

Model features include elevation, corridor isolation, turning conflicts, passenger demand, previous delays, corridor, weather, and peak-hour status. The target is `delay_minutes`.

Metrics from the current training run must not be treated as real-world LRT accuracy because the dataset is synthetic and exists to validate the pipeline.

## Route algorithm

`route_planner.py` contains a weighted station graph and a Dijkstra implementation. Each edge weight is the distance between stations in kilometers. The algorithm returns the optimal station path and its total distance.

## Project structure

```text
├── index.html                # Single-page interactive demo
├── style.css                 # Simulation Lab interface
├── script.js                 # Browser Dijkstra and simulation
├── app.py                    # FastAPI endpoints
├── route_planner.py          # LRT graph and Dijkstra
├── train.py                  # Training and TimeSeriesSplit
├── predict.py                # Local prediction example
├── data_generator.py         # Synthetic data generator
├── visualize.py              # Charts and permutation importance
├── notebooks/01_eda.ipynb    # Exploratory notebook
├── tests/                    # Smoke tests
├── Dockerfile                # Containerized API
└── .github/workflows/ci.yml  # Checks on push and pull request
```

## Checks

```powershell
python -m pytest -q
python -m py_compile app.py route_planner.py train.py predict.py visualize.py data_generator.py
```

CI automatically runs training and tests on every push or pull request.

## Next steps

1. Connect real GTFS/GPS data after checking source licensing and quality.
2. Add SHAP explanations for individual predictions.
3. Add prediction intervals after selecting and validating a quantile model.
4. Replace the demonstration graph with a verified station and interchange map.
5. Publish the API only after adding secrets management, monitoring, and deployment configuration.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
