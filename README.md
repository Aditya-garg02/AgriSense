# 🌱 AgriSense — AI-Powered Agricultural Decision Support System

AgriSense is an AI-powered agricultural decision support system that uses
Machine Learning and agricultural data to provide **crop recommendations**
and **crop yield predictions** based on soil, weather, location, crop and
cultivation-related parameters.

## 🚀 Live Demo

👉 **[Try AgriSense Live](https://aditya-garg02.github.io/AgriSense/)**

> The web version is deployed using GitHub Pages.

---

## ✨ Features

### 🌾 Crop Recommendation

Recommends suitable crops based on:

- State
- District
- Soil type
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Soil pH
- Temperature
- Humidity
- Rainfall

### 📈 Yield Prediction

Predicts expected crop yield using:

- State
- District
- Crop
- Season
- Cultivated area
- Agricultural data

### 🌦️ Weather & Location-Based Data

The system uses district-level agricultural and rainfall information
to improve recommendations.

### 🖥️ Two Interfaces

- **Python Tkinter desktop application**
- **Browser-based web application**

The web application can be accessed directly through the live demo.

---

## 🧠 Machine Learning

AgriSense uses Machine Learning models for:

1. **Crop Recommendation**
2. **Yield Prediction**

The trained models are exported for use by the browser-based application.

---

## 📊 Datasets

The project uses agricultural datasets containing information such as:

- Crop production and yield
- Soil nutrients
- Soil properties
- District rainfall
- Crop requirements

Main datasets:

```text
datasets/
├── APY.xlsx
├── crop_requirements.xlsx
├── district_rainfall.csv
└── soil_data.xlsx
