import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Climate Risk Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DESIGN SYSTEM — Apple × ATSUEIGO Aesthetic
# ============================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --c-bg:          #080808;
    --c-surface:     #111111;
    --c-surface2:    #181818;
    --c-surface3:    #222222;
    --c-border:      rgba(255,255,255,0.07);
    --c-border2:     rgba(255,255,255,0.14);
    --c-text:        #f0f0f0;
    --c-muted:       rgba(240,240,240,0.4);
    --c-faint:       rgba(240,240,240,0.15);
    --c-red:         #ff4d4d;
    --c-orange:      #ff8c42;
    --c-yellow:      #ffd166;
    --c-green:       #06d6a0;
    --c-blue:        #4cc9f0;
    --c-accent:      #ff4d4d;
    --font-display:  'Syne', sans-serif;
    --font-body:     'DM Sans', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius-sm:     8px;
    --radius-md:     16px;
    --radius-lg:     24px;
    --radius-xl:     32px;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--c-bg) !important;
    color: var(--c-text) !important;
    font-family: var(--font-body) !important;
}

/* Remove Streamlit chrome */
header[data-testid="stHeader"]          { display: none !important; }
[data-testid="stSidebarCollapsedControl"]{ display: none !important; }
#MainMenu, footer                        { display: none !important; }
.stDeployButton                          { display: none !important; }
[data-testid="stDecoration"]             { display: none !important; }

/* Block container */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
.stMainBlockContainer {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display) !important;
    color: var(--c-text) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--c-border2); border-radius: 99px; }

/* ── Select box ── */
.stSelectbox > div > div {
    background: var(--c-surface2) !important;
    border: 1px solid var(--c-border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--c-text) !important;
    font-family: var(--font-body) !important;
    font-size: 15px !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--c-border2) !important;
}
[data-baseweb="select"] > div {
    background: var(--c-surface2) !important;
    border-color: var(--c-border2) !important;
}

/* ── Plotly charts ── */
.js-plotly-plot .plotly, .plot-container {
    background: transparent !important;
}

/* ── Columns ── */
[data-testid="column"] { padding: 0 8px !important; }

/* ── Layout wrappers ── */
.page-wrapper {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 48px 80px 48px;
}

/* ============ HERO ============ */
.hero {
    padding: 80px 0 60px 0;
    position: relative;
    overflow: hidden;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--c-muted);
    margin-bottom: 20px;
}
.hero-title {
    font-family: var(--font-display);
    font-size: clamp(56px, 8vw, 108px);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -3px;
    color: var(--c-text);
    margin-bottom: 8px;
}
.hero-title-accent {
    background: linear-gradient(120deg, #ff4d4d 0%, #ff8c42 40%, #ffd166 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: var(--font-body);
    font-size: 16px;
    font-weight: 300;
    color: var(--c-muted);
    letter-spacing: 0.5px;
    margin-top: 24px;
}
.hero-live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(6,214,160,0.1);
    border: 1px solid rgba(6,214,160,0.25);
    border-radius: 99px;
    padding: 5px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--c-green);
    margin-bottom: 32px;
}
.hero-live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--c-green);
    animation: pulse-green 2s ease-in-out infinite;
}
@keyframes pulse-green {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ============ SELECTOR ROW ============ */
.selector-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 48px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--c-border);
}
.selector-label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--c-muted);
    white-space: nowrap;
}

/* ============ RISK SCORE HERO CARD ============ */
.risk-hero-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-xl);
    padding: 56px 64px;
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
}
.risk-hero-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse 60% 80% at 50% -20%,
        rgba(255,77,77,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.risk-card-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--c-muted);
    margin-bottom: 12px;
}
.risk-score-display {
    font-family: var(--font-display);
    font-size: clamp(100px, 14vw, 180px);
    font-weight: 800;
    line-height: 0.85;
    letter-spacing: -6px;
    background: linear-gradient(120deg, #ff4d4d, #ff8c42, #ffd166);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}
.risk-score-max {
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 500;
    color: var(--c-muted);
    vertical-align: super;
    letter-spacing: -1px;
}
.risk-level-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-radius: 99px;
    padding: 8px 20px;
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 24px;
}
.risk-level-extreme {
    background: rgba(255,77,77,0.12);
    border: 1px solid rgba(255,77,77,0.3);
    color: #ff6b6b;
}
.risk-level-high {
    background: rgba(255,140,66,0.12);
    border: 1px solid rgba(255,140,66,0.3);
    color: #ff8c42;
}
.risk-level-moderate {
    background: rgba(255,209,102,0.12);
    border: 1px solid rgba(255,209,102,0.3);
    color: #ffd166;
}
.risk-level-low {
    background: rgba(6,214,160,0.12);
    border: 1px solid rgba(6,214,160,0.3);
    color: #06d6a0;
}
.risk-delta {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--c-muted);
    margin-top: 12px;
}
.risk-delta-up   { color: var(--c-red);   }
.risk-delta-down { color: var(--c-green); }
.risk-breakdown {
    margin-top: 48px;
    padding-top: 32px;
    border-top: 1px solid var(--c-border);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}
.risk-factor {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.risk-factor-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--c-faint);
}
.risk-factor-value {
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 700;
    color: var(--c-text);
    letter-spacing: -1px;
}
.risk-factor-unit {
    font-size: 13px;
    font-weight: 400;
    color: var(--c-muted);
    margin-left: 4px;
}
.risk-factor-bar {
    height: 3px;
    background: var(--c-border);
    border-radius: 99px;
    overflow: hidden;
    margin-top: 4px;
}
.risk-factor-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #ff4d4d, #ffd166);
}

/* ============ KPI CARDS ============ */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.kpi-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 28px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
    cursor: default;
}
.kpi-card:hover {
    border-color: var(--c-border2);
    transform: translateY(-2px);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--c-accent), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.kpi-card:hover::after { opacity: 0.3; }
.kpi-icon {
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--c-faint);
    font-family: var(--font-mono);
    margin-bottom: 20px;
}
.kpi-value {
    font-family: var(--font-display);
    font-size: 48px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -2px;
    color: var(--c-text);
    margin-bottom: 6px;
}
.kpi-unit {
    font-size: 18px;
    font-weight: 400;
    color: var(--c-muted);
    margin-left: 4px;
}
.kpi-label {
    font-size: 13px;
    color: var(--c-muted);
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* ============ SECTION HEADER ============ */
.section-header {
    margin: 48px 0 24px 0;
    display: flex;
    align-items: baseline;
    gap: 16px;
}
.section-title {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--c-text);
}
.section-tag {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--c-faint);
}

/* ============ CONTENT CARDS ============ */
.content-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 32px;
    height: 100%;
}
.content-card-title {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--c-muted);
    margin-bottom: 24px;
}

/* ============ INSIGHTS ============ */
.insight-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 0;
    border-bottom: 1px solid var(--c-border);
}
.insight-item:last-child { border-bottom: none; }
.insight-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}
.insight-text {
    font-size: 14px;
    line-height: 1.7;
    color: rgba(240,240,240,0.7);
    font-weight: 300;
}
.insight-text strong {
    color: var(--c-text);
    font-weight: 500;
}

/* ============ HEALTH GUIDANCE ============ */
.health-card {
    background: var(--c-surface2);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 10px;
    border-left: 3px solid;
}
.health-card-title {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.health-card-body {
    font-size: 14px;
    font-weight: 300;
    line-height: 1.7;
    color: rgba(240,240,240,0.65);
}

/* ============ RANKING ============ */
.rank-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0;
    border-bottom: 1px solid var(--c-border);
}
.rank-item:last-child { border-bottom: none; }
.rank-left {
    display: flex;
    align-items: center;
    gap: 16px;
}
.rank-num {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--c-faint);
    width: 20px;
}
.rank-city {
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 600;
    letter-spacing: -0.3px;
}
.rank-score {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -1px;
}

/* ============ PREDICTION CARD ============ */
.pred-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-xl);
    padding: 48px;
    position: relative;
    overflow: hidden;
}
.pred-card::before {
    content: '';
    position: absolute;
    bottom: -40%; right: -10%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(76,201,240,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.pred-score-main {
    font-family: var(--font-display);
    font-size: 80px;
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 0.9;
    color: var(--c-text);
    margin: 16px 0 8px 0;
}
.pred-confidence {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(76,201,240,0.08);
    border: 1px solid rgba(76,201,240,0.2);
    border-radius: 99px;
    padding: 5px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--c-blue);
    margin-top: 16px;
}
.pred-factors {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--c-border);
}
.pred-factor-tag {
    display: inline-block;
    background: var(--c-surface2);
    border: 1px solid var(--c-border2);
    border-radius: var(--radius-sm);
    padding: 6px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 1px;
    color: rgba(240,240,240,0.6);
    margin: 4px 4px 4px 0;
}

/* ============ FORECAST NUMBERS ============ */
.forecast-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 24px;
}
.forecast-item {
    background: var(--c-surface2);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-md);
    padding: 24px;
    text-align: center;
}
.forecast-period {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--c-faint);
    text-transform: uppercase;
    margin-bottom: 12px;
}
.forecast-score {
    font-family: var(--font-display);
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
    color: var(--c-text);
}
.forecast-label {
    font-size: 12px;
    color: var(--c-muted);
    margin-top: 8px;
    font-weight: 300;
}

/* ============ DIVIDER ============ */
.divider {
    height: 1px;
    background: var(--c-border);
    margin: 40px 0;
}

/* ============ FOOTER ============ */
.footer {
    padding: 32px 0 0 0;
    border-top: 1px solid var(--c-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 64px;
}
.footer-left {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--c-faint);
    text-transform: uppercase;
}
.footer-right {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--c-faint);
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# DATA & CALCULATIONS
# ============================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("climate_data.csv")
    except FileNotFoundError:
        data = {
            "city": ["Tokyo","Beijing","Bangkok","Seoul","Delhi","Singapore",
                     "Dhaka","Ulaanbaatar","Berlin","London","Reykjavik",
                     "New York","Sydney","Nairobi","Jakarta"],
            "lat":  [35.68,39.90,13.76,37.57,28.61,1.35,23.81,47.89,
                     52.52,51.51,64.13,40.71,-33.87,-1.29,-6.21],
            "lon":  [139.65,116.41,100.50,126.98,77.21,103.82,90.41,106.91,
                     13.41,-0.13,-21.82,-74.01,151.21,36.82,106.85],
            "temperature": [28.5,35.2,33.8,26.4,38.7,30.2,32.4,22.1,
                            18.3,16.8, 8.4,22.6,24.8,25.6,31.5],
            "pm25": [18.2,89.4,45.6,38.9,178.3,22.4,112.5,76.8,
                     14.2,12.8,  5.2,18.9, 11.4,28.4, 67.8],
            "aqi":  [72,156,98,88,285,65,198,134,45,38,18,58,42,71,122],
            "humidity": [68,42,75,55,34,82,71,38,72,78,65,62,70,66,79],
        }
        df = pd.DataFrame(data)
    return df

def compute_risk_score(row):
    temp_deviation = max(0, abs(row["temperature"] - 22) - 5) * 2
    temp_score     = min(temp_deviation / 30 * 100, 100)
    pm25_score     = min(row["pm25"] / 200 * 100, 100)
    aqi_score      = min(row["aqi"] / 300 * 100, 100)
    hum            = row["humidity"]
    hum_score      = min(abs(hum - 55) / 45 * 100, 100) if hum > 55 else min(abs(hum-55)/55*100, 100)
    score = pm25_score*0.40 + temp_score*0.30 + hum_score*0.20 + aqi_score*0.10
    return round(min(score, 100), 1)

def get_risk_level(score):
    if score >= 75: return "EXTREME", "#ff4d4d",  "risk-level-extreme"
    if score >= 55: return "HIGH",    "#ff8c42",  "risk-level-high"
    if score >= 35: return "MODERATE","#ffd166",  "risk-level-moderate"
    return              "LOW",     "#06d6a0",  "risk-level-low"

def generate_trend_data(base_score, n=48):
    np.random.seed(42)
    trend = np.cumsum(np.random.randn(n) * 1.5) * 0.3
    seasonal = np.sin(np.linspace(0, 4*np.pi, n)) * 3
    scores = np.clip(base_score + trend + seasonal + np.random.randn(n)*0.8, 0, 100)
    times = [datetime.now() - timedelta(hours=n-i) for i in range(n)]
    return times, scores.tolist()

def cross_city_predict(df, city_row, exclude_city):
    candidates = df[df["city"] != exclude_city].copy()
    dist = np.sqrt((candidates["pm25"] - city_row["pm25"])**2 +
                   (candidates["temperature"] - city_row["temperature"])**2)
    candidates["distance"] = dist
    candidates["risk_score"] = candidates.apply(compute_risk_score, axis=1)
    top3 = candidates.nsmallest(3, "distance")
    global_base = candidates["risk_score"].mean()
    weighted = (top3["risk_score"] * (1 / (top3["distance"] + 1))).sum() / \
               (1 / (top3["distance"] + 1)).sum()
    predicted = weighted * 0.7 + global_base * 0.3
    confidence = max(50, min(92, 92 - dist.min() * 0.8))
    trend_dir = "↑ RISING" if city_row["pm25"] > global_base * 0.5 else "↓ STABLE"
    factors = []
    if city_row["pm25"] > 50: factors.append("HIGH PM2.5")
    if abs(city_row["temperature"] - 22) > 10: factors.append("TEMP ANOMALY")
    if city_row["humidity"] > 75: factors.append("HIGH HUMIDITY")
    if city_row["aqi"] > 100: factors.append("POOR AQI")
    if not factors: factors = ["BASELINE CONDITIONS"]
    similar = top3["city"].tolist()
    return round(predicted, 1), round(confidence, 1), trend_dir, factors, similar

# ============================================================
# LOAD & COMPUTE
# ============================================================
df = load_data()
df["risk_score"] = df.apply(compute_risk_score, axis=1)

CITIES = sorted(df["city"].tolist())
now_str = datetime.now().strftime("%Y · %m · %d  %H:%M")

# ============================================================
# PAGE
# ============================================================
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-live-badge">
    <div class="hero-live-dot"></div>
    LIVE · {now_str}
  </div>
  <p class="hero-eyebrow">Environmental Risk Quantification System</p>
  <h1 class="hero-title">
    Climate Risk<br>
    <span class="hero-title-accent">Intelligence</span>
  </h1>
  <p class="hero-sub">
    Real-time atmospheric analysis across 15 global cities.<br>
    PM2.5 · Temperature · Humidity · AQI
  </p>
</div>
""", unsafe_allow_html=True)

# ── CITY SELECTOR ─────────────────────────────────────────────
st.markdown('<div class="selector-row"><span class="selector-label">Select City →</span></div>',
            unsafe_allow_html=True)
col_sel, col_pad = st.columns([2, 5])
with col_sel:
    selected_city = st.selectbox(
        "", CITIES,
        index=CITIES.index("Tokyo"),
        label_visibility="collapsed"
    )

# ── DATA FOR SELECTED CITY ────────────────────────────────────
row = df[df["city"] == selected_city].iloc[0]
risk_score = row["risk_score"]
risk_label, risk_color, risk_class = get_risk_level(risk_score)
prev_score = risk_score + (random.uniform(-5, 5))
delta = risk_score - prev_score
delta_class = "risk-delta-up" if delta > 0 else "risk-delta-down"
delta_arrow = "↑" if delta > 0 else "↓"

# ── RISK HERO CARD ────────────────────────────────────────────
temp_pct  = min(max(abs(row["temperature"]-22)/30, 0), 1) * 100
pm25_pct  = min(row["pm25"]/200, 1) * 100
aqi_pct   = min(row["aqi"]/300, 1) * 100
hum_pct   = min(abs(row["humidity"]-55)/45, 1) * 100

st.markdown(f"""
<div class="risk-hero-card">
  <p class="risk-card-eyebrow">Climate Risk Score · {selected_city.upper()}</p>
  <div style="display:flex;align-items:flex-end;gap:8px;line-height:1;">
    <span class="risk-score-display">{risk_score:.0f}</span>
    <span class="risk-score-max">/ 100</span>
  </div>
  <div class="risk-level-badge {risk_class}">
    <span style="width:7px;height:7px;border-radius:50%;background:{risk_color};
                 display:inline-block;flex-shrink:0;"></span>
    {risk_label} RISK
  </div>
  <p class="risk-delta">
    <span class="{delta_class}">{delta_arrow} {abs(delta):.1f} pts</span>
    &nbsp;·&nbsp; vs 24h ago
  </p>

  <div class="risk-breakdown">
    <div class="risk-factor">
      <span class="risk-factor-label">PM 2.5 · 40%</span>
      <span class="risk-factor-value">{row['pm25']:.1f}<span class="risk-factor-unit">μg/m³</span></span>
      <div class="risk-factor-bar"><div class="risk-factor-fill" style="width:{pm25_pct:.0f}%"></div></div>
    </div>
    <div class="risk-factor">
      <span class="risk-factor-label">Temperature · 30%</span>
      <span class="risk-factor-value">{row['temperature']:.1f}<span class="risk-factor-unit">°C</span></span>
      <div class="risk-factor-bar"><div class="risk-factor-fill" style="width:{temp_pct:.0f}%"></div></div>
    </div>
    <div class="risk-factor">
      <span class="risk-factor-label">Humidity · 20%</span>
      <span class="risk-factor-value">{row['humidity']:.0f}<span class="risk-factor-unit">%</span></span>
      <div class="risk-factor-bar"><div class="risk-factor-fill" style="width:{hum_pct:.0f}%"></div></div>
    </div>
    <div class="risk-factor">
      <span class="risk-factor-label">AQI · 10%</span>
      <span class="risk-factor-value">{row['aqi']:.0f}<span class="risk-factor-unit">idx</span></span>
      <div class="risk-factor-bar"><div class="risk-factor-fill" style="width:{aqi_pct:.0f}%"></div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────
kpi_data = [
    ("PM 2.5", f"{row['pm25']:.1f}", "μg/m³",    "Air Quality Index"),
    ("Temp",   f"{row['temperature']:.1f}", "°C",  "Surface Temperature"),
    ("Humidity",f"{row['humidity']:.0f}",  "%",    "Relative Humidity"),
    ("AQI",    f"{row['aqi']:.0f}",        "",     "Air Quality Index"),
]
cols = st.columns(4)
for col, (label, val, unit, desc) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon">{label}</div>
          <div class="kpi-value">{val}<span class="kpi-unit">{unit}</span></div>
          <div class="kpi-label">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── HEALTH GUIDANCE ───────────────────────────────────────────
st.markdown("""<div class="section-header">
  <span class="section-title">Health Guidance</span>
  <span class="section-tag">Automated · Real-Time</span>
</div>""", unsafe_allow_html=True)

guidance = []
if risk_score >= 75:
    guidance = [
        ("CRITICAL", "red", "#ff4d4d",
         "Avoid all outdoor activities. N95 mask mandatory if outdoors."),
        ("ALERT", "red", "#ff6b6b",
         "Windows and doors should remain closed. Use air purifiers on maximum setting."),
        ("MEDICAL", "orange", "#ff8c42",
         "Individuals with respiratory conditions should consult healthcare providers immediately."),
    ]
elif risk_score >= 55:
    guidance = [
        ("WARNING", "orange", "#ff8c42",
         "Limit prolonged outdoor exertion. Sensitive groups should stay indoors."),
        ("ADVISORY", "yellow", "#ffd166",
         "Wear a face mask when outdoors for extended periods."),
        ("HYDRATION", "blue", "#4cc9f0",
         "Maintain hydration levels above 2.5L daily due to atmospheric conditions."),
    ]
elif risk_score >= 35:
    guidance = [
        ("CAUTION", "yellow", "#ffd166",
         "Air quality is acceptable for most. Unusual sensitivity may cause minor concern."),
        ("ACTIVITY", "green", "#06d6a0",
         "Moderate outdoor exercise is permitted. Monitor symptoms."),
    ]
else:
    guidance = [
        ("CLEAR", "green", "#06d6a0",
         "Air quality and environmental conditions are favorable today."),
        ("ACTIVITY", "green", "#06d6a0",
         "All outdoor activities are recommended. Ideal conditions for exercise."),
    ]

for tag, color_name, color_hex, text in guidance:
    st.markdown(f"""
    <div class="health-card" style="border-left-color:{color_hex}">
      <div class="health-card-title" style="color:{color_hex}">{tag}</div>
      <div class="health-card-body">{text}</div>
    </div>
    """, unsafe_allow_html=True)

# ── TREND + MAP ───────────────────────────────────────────────
st.markdown("""<div class="section-header">
  <span class="section-title">Risk Trend · Global Map</span>
  <span class="section-tag">48h Window</span>
</div>""", unsafe_allow_html=True)

col_trend, col_map = st.columns([1, 1], gap="medium")

with col_trend:
    st.markdown('<div class="content-card"><p class="content-card-title">Risk Score · 48h History</p>',
                unsafe_allow_html=True)
    times, scores = generate_trend_data(risk_score)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=times, y=scores,
        mode="lines",
        line=dict(color="#ff4d4d", width=2),
        fill="tozeroy",
        fillcolor="rgba(255,77,77,0.06)",
        hovertemplate="%{y:.1f}<extra></extra>"
    ))
    # Threshold lines
    for level, color, label in [(75,"#ff4d4d","EXTREME"),(55,"#ff8c42","HIGH"),(35,"#ffd166","MODERATE")]:
        fig_trend.add_hline(y=level, line=dict(color=color, width=1, dash="dot"),
                             annotation_text=label,
                             annotation_font=dict(size=9, color=color),
                             annotation_position="right")
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=0, b=0),
        height=280,
        xaxis=dict(showgrid=False, color="rgba(255,255,255,0.2)",
                   tickfont=dict(size=10, family="JetBrains Mono")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                   color="rgba(255,255,255,0.2)",
                   tickfont=dict(size=10, family="JetBrains Mono"),
                   range=[0, 105]),
        font=dict(family="JetBrains Mono"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_map:
    st.markdown('<div class="content-card"><p class="content-card-title">Global Risk Distribution</p>',
                unsafe_allow_html=True)
    def score_to_color(s):
        if s >= 75: return "#ff4d4d"
        if s >= 55: return "#ff8c42"
        if s >= 35: return "#ffd166"
        return "#06d6a0"

    fig_map = go.Figure(go.Scattermap(
        lat=df["lat"], lon=df["lon"],
        mode="markers+text",
        marker=dict(
            size=df["risk_score"] / 5 + 8,
            color=df["risk_score"],
            colorscale=[[0,"#06d6a0"],[0.35,"#ffd166"],[0.55,"#ff8c42"],[1,"#ff4d4d"]],
            cmin=0, cmax=100,
            opacity=0.85,
            showscale=False,
        ),
        text=df["city"],
        textfont=dict(size=9, color="rgba(255,255,255,0.6)", family="JetBrains Mono"),
        textposition="top center",
        customdata=df["risk_score"],
        hovertemplate="<b>%{text}</b><br>Risk Score: %{customdata:.1f}<extra></extra>",
    ))
    fig_map.update_layout(
        map=dict(
            style="carto-darkmatter",
            center=dict(lat=20, lon=20),
            zoom=0.8,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=280,
        font=dict(family="JetBrains Mono"),
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ── RANKINGS ─────────────────────────────────────────────────
st.markdown("""<div class="section-header">
  <span class="section-title">City Risk Rankings</span>
  <span class="section-tag">15 Cities · Current</span>
</div>""", unsafe_allow_html=True)

col_top, col_low = st.columns(2, gap="medium")
top5 = df.nlargest(5, "risk_score")[["city","risk_score"]]
low5 = df.nsmallest(5, "risk_score")[["city","risk_score"]]

with col_top:
    st.markdown('<div class="content-card"><p class="content-card-title">Highest Risk Cities</p>',
                unsafe_allow_html=True)
    for i, (_, r) in enumerate(top5.iterrows(), 1):
        lbl, col_hex, _ = get_risk_level(r["risk_score"])
        st.markdown(f"""
        <div class="rank-item">
          <div class="rank-left">
            <span class="rank-num">{i:02d}</span>
            <span class="rank-city">{r['city']}</span>
          </div>
          <span class="rank-score" style="color:{col_hex}">{r['risk_score']:.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_low:
    st.markdown('<div class="content-card"><p class="content-card-title">Lowest Risk Cities</p>',
                unsafe_allow_html=True)
    for i, (_, r) in enumerate(low5.iterrows(), 1):
        lbl, col_hex, _ = get_risk_level(r["risk_score"])
        st.markdown(f"""
        <div class="rank-item">
          <div class="rank-left">
            <span class="rank-num">{i:02d}</span>
            <span class="rank-city">{r['city']}</span>
          </div>
          <span class="rank-score" style="color:{col_hex}">{r['risk_score']:.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── AI INSIGHTS ───────────────────────────────────────────────
st.markdown("""<div class="section-header">
  <span class="section-title">AI Insights</span>
  <span class="section-tag">System Generated</span>
</div>""", unsafe_allow_html=True)

pm25_rank  = int(df["pm25"].rank(ascending=False)[df["city"]==selected_city].values[0])
risk_rank  = int(df["risk_score"].rank(ascending=False)[df["city"]==selected_city].values[0])
avg_global = df["risk_score"].mean()

insights = [
    ("#ff4d4d", f"<strong>{selected_city}</strong> ranks <strong>#{risk_rank}</strong> globally "
                f"out of 15 cities with a risk score of <strong>{risk_score:.1f}/100</strong>."),
    ("#ff8c42", f"PM2.5 concentration of <strong>{row['pm25']:.1f} μg/m³</strong> is the "
                f"<strong>{'above' if row['pm25'] > df['pm25'].mean() else 'below'} global average</strong> "
                f"({df['pm25'].mean():.1f} μg/m³)."),
    ("#ffd166", f"Current risk score is <strong>{abs(risk_score - avg_global):.1f} points "
                f"{'above' if risk_score > avg_global else 'below'}</strong> the global average of "
                f"<strong>{avg_global:.1f}</strong>."),
    ("#4cc9f0", f"Temperature deviation of <strong>{abs(row['temperature']-22):.1f}°C</strong> "
                f"from optimal baseline (22°C) contributes <strong>30%</strong> to the risk model."),
]

st.markdown('<div class="content-card">', unsafe_allow_html=True)
for color, text in insights:
    st.markdown(f"""
    <div class="insight-item">
      <div class="insight-dot" style="background:{color}"></div>
      <span class="insight-text">{text}</span>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── CROSS-CITY PREDICTION ─────────────────────────────────────
st.markdown("""<div class="section-header">
  <span class="section-title">Cross-City Prediction Engine</span>
  <span class="section-tag">ML · Similarity-Weighted</span>
</div>""", unsafe_allow_html=True)

pred_score, pred_conf, trend_dir, factors, similar_cities = cross_city_predict(df, row, selected_city)
pred_label, pred_color, pred_class = get_risk_level(pred_score)
factor_tags = "".join([f'<span class="pred-factor-tag">{f}</span>' for f in factors])
similar_tags = "".join([f'<span class="pred-factor-tag">{c}</span>' for c in similar_cities])

col_pred, col_fore = st.columns([1, 1], gap="medium")

with col_pred:
    st.markdown(f"""
    <div class="pred-card">
      <p class="content-card-title">Predicted Risk · 24h Forecast</p>
      <div class="risk-level-badge {pred_class}" style="margin-top:0">
        <span style="width:7px;height:7px;border-radius:50%;background:{pred_color};
                     display:inline-block;"></span>
        {pred_label}
      </div>
      <div class="pred-score-main">{pred_score:.0f}</div>
      <span class="pred-confidence">CONFIDENCE &nbsp; {pred_conf:.0f}%</span>
      <p style="font-family:var(--font-mono);font-size:12px;color:var(--c-muted);
                letter-spacing:2px;margin-top:12px;">{trend_dir}</p>
      <div class="pred-factors">
        <p style="font-family:var(--font-mono);font-size:10px;letter-spacing:3px;
                  color:var(--c-faint);text-transform:uppercase;margin-bottom:10px;">
          Contributing Factors
        </p>
        {factor_tags}
        <p style="font-family:var(--font-mono);font-size:10px;letter-spacing:3px;
                  color:var(--c-faint);text-transform:uppercase;margin:16px 0 10px 0;">
          Similar Cities Used
        </p>
        {similar_tags}
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_fore:
    st.markdown('<div class="content-card"><p class="content-card-title">Multi-Period Forecast</p>',
                unsafe_allow_html=True)
    periods = [
        ("6h",  pred_score * 0.95 + risk_score * 0.05),
        ("12h", pred_score * 0.80 + risk_score * 0.20),
        ("24h", pred_score),
        ("48h", pred_score * 0.85 + avg_global * 0.15),
        ("72h", pred_score * 0.70 + avg_global * 0.30),
        ("7d",  avg_global * 0.60 + pred_score * 0.40),
    ]
    fig_fore = go.Figure()
    xs = [p[0] for p in periods]
    ys = [p[1] for p in periods]
    fig_fore.add_trace(go.Bar(
        x=xs, y=ys,
        marker_color=[score_to_color(s) for s in ys],
        marker_line_width=0,
        opacity=0.8,
        text=[f"{s:.0f}" for s in ys],
        textposition="outside",
        textfont=dict(size=11, color="rgba(255,255,255,0.6)", family="JetBrains Mono"),
        hovertemplate="%{x}: %{y:.1f}<extra></extra>",
    ))
    fig_fore.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=320,
        bargap=0.3,
        xaxis=dict(showgrid=False, color="rgba(255,255,255,0.25)",
                   tickfont=dict(size=10, family="JetBrains Mono")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                   color="rgba(255,255,255,0.25)",
                   tickfont=dict(size=10, family="JetBrains Mono"),
                   range=[0, 115]),
        font=dict(family="JetBrains Mono"),
    )
    st.plotly_chart(fig_fore, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div class="footer-left">Climate Risk Intelligence · Created by YUKI · v3.0</div>
  <div class="footer-right">{now_str} UTC · 15 Cities · 4 Variables</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # page-wrapper
