# 🌍 Climate Risk Intelligence

### AI-Powered Environmental Risk Quantification System

<p align="center">
  <img src="https://img.shields.io/badge/version-3.0-ff4d4d?style=flat-square">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square">
  <img src="https://img.shields.io/badge/streamlit-1.58.0-FF4B4B?style=flat-square">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square">
</p>

<p align="center">
  <a href="https://climate-risk-intelligence.streamlit.app"><strong>🔗 Live Demo</strong></a>
</p>

---

## 🧠 Overview

**Climate Risk Intelligence** is a research prototype that transforms raw environmental data into a **single, interpretable Climate Risk Score (0–100)**.

It integrates:
- **PM2.5** (40%) — Air pollution concentration
- **Temperature Anomaly** (30%) — Deviation from optimal 22°C
- **Humidity Stress** (20%) — Deviation from optimal 55%
- **AQI** (10%) — Composite air quality index

> **Not just data. Decisions.**

---

## 🔥 Key Features

### 🎯 Climate Risk Score Engine
A novel composite index weighting 4 environmental factors into one actionable number.

### 🗺 Global Risk Visualization
Interactive dark-theme Mapbox with 15 cities. Green → Yellow → Orange → Red risk gradient.

### 📈 48h Risk Trend Analysis
Simulated time-series with seasonal + stochastic modeling. Threshold-based risk levels.

### 🤖 Cross-City Prediction Engine
Similarity-weighted model predicts tomorrow's risk **without historical data**. 88–92% confidence.

### 🧠 AI Insights Generator
Auto-generated: city rankings, pollution deviation, global comparison, risk contribution.

### 📉 Multi-Period Forecast
Predicts risk for 6h / 12h / 24h / 48h / 72h / 7d horizons.

### 🏥 Health Guidance
Auto-generated health advisories based on risk level (Low / Moderate / High / Extreme).

---

## 🏗️ System Architecture
Data Layer Processing Layer Analytics Layer Presentation
(15 cities, CSV) → (Risk scoring, → (Trend simulation, → (Streamlit +
normalization, cross-city pred, Plotly dashboard)
similarity) forecast)

text

---

## 🧮 Risk Model
Risk Score = PM2.5×0.40 + Temperature_Anomaly×0.30 + Humidity_Deviation×0.20 + AQI×0.10

text

| Score | Level | Color |
|-------|-------|-------|
| 0–34 | 🟢 Low | Safe |
| 35–54 | 🟡 Moderate | Caution |
| 55–74 | 🟠 High | Limit exposure |
| 75–100 | 🔴 Extreme | Hazardous |

---

## 🌐 Tech Stack

| Layer | Technology |
|-------|------------|
| UI Framework | Streamlit |
| Data | Pandas, NumPy |
| Visualization | Plotly, Mapbox |
| Typography | Syne, DM Sans, JetBrains Mono |
| Design | Apple-inspired dark theme, ATSUEIGO aesthetic |

---

## ⚡ Quick Start

```bash
git clone https://github.com/yubi-26/climate-risk-intelligence.git
cd climate-risk-intelligence
pip install -r requirements.txt
streamlit run dashboard.py
📁 Project Structure
text
├── dashboard.py          # Main application
├── climate_data.csv      # 15 cities dataset
├── requirements.txt      # Python dependencies
└── README.md
🎯 Design Philosophy
One screen = one narrative

Risk Score as primary visual anchor

All charts serve the main decision

Minimal cognitive load, maximum clarity

"Not just data. Decisions."

🚀 Future Roadmap
Real-time API integration (Open-Meteo, WAQI)

LSTM deep learning forecasting

Satellite data fusion (MODIS, Sentinel-5P)

Email/Push alert system

Expand to 50+ cities

Mobile-responsive layout

📊 Example Output
City	Risk Score	Level
Delhi	76	🔴 Extreme
Beijing	44	🟡 Moderate
Tokyo	15	🟢 Low
Reykjavik	8	🟢 Low
🧠 Research Value
This project demonstrates:

Novel composite index design for environmental health

Spatial cross-city pattern analysis as temporal data substitute

Human-centered risk visualization with Decision-First philosophy

Interpretable ML-inspired systems for public health applications

📌 Author
Built as a Climate Data Intelligence Research Prototype.

Focus: Environmental Analytics · Risk Quantification · AI-Assisted Decision Systems

📄 License
MIT — Free to use, modify, and distribute.