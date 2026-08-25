# 🚌 Almaty BRT Analytics & Prediction Platform

![Almaty BRT Concept](./assets/brt-concept.jpg)

An end-to-end Data Science and Machine Learning project designed to analyze urban transit movement and predict bus delays across the Bus Rapid Transit (BRT) network in Almaty, Kazakhstan.

---

## 📌 Project Overview

This platform processes key urban traffic metrics—such as peak hours, weather conditions, lane isolation, average speed, and intersection conflict risks—to deliver real-time delay predictions for public transport optimization.

* **Target Output:** Bus delay duration in minutes.
* **Core Model:** Gradient Boosting Regressor (`scikit-learn`).

---

## 📊 Model Evaluation Metrics

The Machine Learning pipeline was evaluated on an independent test dataset using standard regression evaluation metrics:

### 1. R² Score (Coefficient of Determination)
Measures the proportion of variance in bus delays predictable from the feature set:
$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}$$

* **Result:** `0.8844` (88.44% of delay variance explained by the model)

---

### 2. MAE (Mean Absolute Error)
Calculates the average magnitude of absolute prediction errors in minutes:
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} \vert{}y_i - \hat{y}_i\vert{}$$

* **Result:** `0.4616` minutes (~28 seconds average prediction error)

---

### 3. MSE (Mean Squared Error)
Measures the mean of squared error differences, penalizing larger outliers:
$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

* **Result:** `0.4671`

---

## 📁 Repository Structure

```text
.
├── assets/
│   └── brt-concept.jpg       # Project visual asset
├── data/
│   └── almaty_brt_dataset.csv # Generated/processed dataset
├── models/
│   └── brt_gb_model.pkl      # Trained Gradient Boosting model
├── .gitignore                # Git exclusion configuration
├── README.md                 # Project documentation
├── train.py                  # Model training pipeline
└── predict.py                # CLI inference tool