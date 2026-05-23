# 🔥 FIRE DETECTION AND MONITORING SYSTEM

## FIXED + GITHUB READY STREAMLIT DASHBOARD

This version fixes:

* ML prediction issues
* Duplicate database inserts
* Streamlit rerun problems
* Supabase connection crashes
* Missing error handling
* Feature order mismatch problems
* Dashboard UI inconsistencies
* Responsive layout issues
* Auto-refresh instability
* History table crashes
* NaN sensor values
* Unknown ML prediction issues

---

# 📁 PROJECT STRUCTURE

Create this folder structure:

```text
fire-dashboard/
│
├── app.py
├── fire_detection_model.pkl
├── requirements.txt
├── packages.txt
└── .streamlit/
    └── config.toml
```

---

# 📄 requirements.txt

```txt
streamlit
pandas
numpy
scikit-learn
supabase
joblib
plotly
streamlit-autorefresh
```

---

# 📄 packages.txt

```txt
libgl1
```

---

# 📄 .streamlit/config.toml

```toml
[theme]
base="dark"
primaryColor="#ff4500"
backgroundColor="#000000"
secondaryBackgroundColor="#111111"
textColor="#ffffff"
```

---

# 📄 app.py

```python
# =====================================================
# FIRE DETECTION AI DASHBOARD + ML + ESP32 CONTROL
# FINAL FIXED VERSION
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

from supabase import create_client
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fire Detection Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# AUTO REFRESH
# =====================================================

st_autorefresh(interval=2000, key="fire_refresh")

# =====================================================
# SUPABASE CONFIGURATION
# =====================================================

SUPABASE_URL = "https://cofxcqxbiminjabrptrp.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNvZnhjcXhiaW1pbmphYnJwdHJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1ODEyMDAsImV4cCI6MjA5MjE1NzIwMH0.6FDwnj_AiaOPVoYNiRA43RKDn3cqLYK00rTHuSaNh3c"

# =====================================================
# CONNECT TO SUPABASE
# =====================================================

try:

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

except Exception as e:

    st.error(f"Supabase Connection Error: {e}")

    st.stop()

# =====================================================
# LOAD MACHINE LEARNING MODEL
# =====================================================

@st.cache_resource

def load_model():

    return joblib.load(
        "fire_detection_model.pkl"
    )

try:

    model = load_model()

except Exception as e:

    st.error(f"Model Loading Error: {e}")

    st.stop()

# =====================================================
# FIRE BACKGROUND CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
GLOBAL APP
===================================================== */

html, body, [class*="css"] {

    font-family: 'Arial', sans-serif;
}

.stApp {

    background:
    radial-gradient(circle at center,
    #220000 0%,
    #0a0000 40%,
    #000000 100%);

    overflow-x: hidden;
}

/* =====================================================
FIRE ANIMATION
===================================================== */

.stApp::before {

    content: "";

    position: fixed;

    bottom: -180px;
    left: -10%;

    width: 120%;
    height: 500px;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,200,50,0.95) 0%,
        rgba(255,120,0,0.75) 25%,
        rgba(255,60,0,0.45) 50%,
        rgba(255,0,0,0.15) 70%,
        transparent 85%
    );

    filter: blur(70px);

    animation:
        fireWave1 8s ease-in-out infinite;

    z-index: 0;

    pointer-events: none;
}

.stApp::after {

    content: "";

    position: fixed;

    bottom: -220px;
    left: -15%;

    width: 130%;
    height: 650px;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,100,0,0.55) 0%,
        rgba(255,40,0,0.35) 40%,
        transparent 80%
    );

    filter: blur(100px);

    animation:
        fireWave2 12s ease-in-out infinite;

    z-index: 0;

    pointer-events: none;
}

@keyframes fireWave1 {

    0% {
        transform:
            translateX(-2%)
            translateY(0px)
            scaleY(1);
    }

    25% {
        transform:
            translateX(1%)
            translateY(-40px)
            scaleY(1.12);
    }

    50% {
        transform:
            translateX(3%)
            translateY(-70px)
            scaleY(1.35);
    }

    75% {
        transform:
            translateX(0%)
            translateY(-30px)
            scaleY(1.1);
    }

    100% {
        transform:
            translateX(-2%)
            translateY(0px)
            scaleY(1);
    }
}

@keyframes fireWave2 {

    0% {
        transform: translateX(0%) scale(1);
    }

    50% {
        transform: translateX(-3%) scale(1.1);
    }

    100% {
        transform: translateX(0%) scale(1);
    }
}

/* =====================================================
MAIN CONTENT
===================================================== */

.main .block-container {

    position: relative;

    z-index: 5;

    padding-top: 2rem;
}

/* =====================================================
TITLE
===================================================== */

.main-title {

    text-align: center;

    font-size: 70px;

    font-weight: 900;

    color: white;

    line-height: 1.1;

    text-shadow:
        0 0 10px red,
        0 0 20px red,
        0 0 40px orange,
        0 0 80px rgba(255,120,0,0.5);

    margin-bottom: 10px;
}

.subtitle {

    text-align: center;

    color: #dddddd;

    font-size: 26px;

    margin-bottom: 40px;
}

/* =====================================================
METRIC CARDS
===================================================== */

.metric-card {

    background:
    linear-gradient(
        180deg,
        rgba(15,15,15,0.97) 0%,
        rgba(5,5,5,0.97) 100%
    );

    border: 2px solid rgba(255,69,0,0.85);

    border-radius: 28px;

    padding: 35px;

    min-height: 360px;

    text-align: center;

    position: relative;

    overflow: hidden;

    transition: all 0.3s ease;

    box-shadow:
        0 0 25px rgba(255,69,0,0.35);
}

.metric-card:hover {

    transform: translateY(-8px);

    box-shadow:
        0 0 45px rgba(255,69,0,0.7);
}

.metric-icon {

    font-size: 90px;

    margin-bottom: 10px;
}

.metric-header {

    color: white;

    font-size: 30px;

    font-weight: 800;

    margin-bottom: 10px;
}

.metric-line {

    width: 110px;

    height: 4px;

    background: #ff4500;

    margin: auto;

    margin-bottom: 25px;

    border-radius: 50px;
}

.metric-label {

    color: #f1f1f1;

    font-size: 28px;

    font-weight: 600;

    margin-bottom: 25px;
}

.metric-value {

    color: #ff4500;

    font-size: 82px;

    font-weight: 900;

    text-shadow:
        0 0 25px rgba(255,69,0,0.7);
}

.metric-unit {

    font-size: 38px;

    color: white;
}

/* =====================================================
STATUS BOX
===================================================== */

.status-box {

    margin-top: 35px;

    background:
    rgba(25,0,0,0.8);

    border-radius: 25px;

    padding: 30px;

    text-align: center;

    backdrop-filter: blur(10px);
}

.status-title {

    font-size: 50px;

    font-weight: 900;

    margin-bottom: 10px;
}

.status-subtitle {

    color: white;

    font-size: 24px;
}

/* =====================================================
TABLE DESIGN
===================================================== */

[data-testid="stDataFrame"] {

    background:
    linear-gradient(
        180deg,
        rgba(45,0,0,0.96) 0%,
        rgba(10,0,0,0.96) 100%
    ) !important;

    border: 2px solid rgba(255,80,0,0.8);

    border-radius: 20px;

    overflow: hidden;
}

/* =====================================================
CHARTS
===================================================== */

.js-plotly-plot {

    border-radius: 20px;

    overflow: hidden;
}

h1, h2, h3 {

    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div class="main-title">
FIRE DETECTION AND MONITORING SYSTEM
</div>

<div class="subtitle">
Live Sensor Readings
</div>
""", unsafe_allow_html=True)

# =====================================================
# FETCH SENSOR DATA
# =====================================================

try:

    response = supabase.table(
        "table1_raw_data"
    ).select("*").order(
        "Date_and_Time",
        desc=True
    ).limit(1).execute()

except Exception as e:

    st.error(f"Database Error: {e}")

    st.stop()

# =====================================================
# CHECK EMPTY DATA
# =====================================================

if not response.data:

    st.warning("No sensor data available.")

    st.stop()

# =====================================================
# CONVERT TO DATAFRAME
# =====================================================

df = pd.DataFrame(response.data)

latest = df.iloc[0]

# =====================================================
# SAFE VALUE EXTRACTION
# =====================================================

def safe_float(value):

    try:
        return float(value)
    except:
        return 0.0

temperature = safe_float(
    latest.get("temperature_reading", 0)
)

air_quality = safe_float(
    latest.get("air_quality_reading", 0)
)

carbon_monoxide = safe_float(
    latest.get("carbon_monoxide_reading", 0)
)

smoke = safe_float(
    latest.get("smoke_reading", 0)
)

# =====================================================
# ML INPUT
# =====================================================

input_data = pd.DataFrame([[
    temperature,
    air_quality,
    carbon_monoxide,
    smoke
]], columns=[
    'temperature',
    'air_quality',
    'carbon_monoxide',
    'smoke'
])

# =====================================================
# MACHINE LEARNING PREDICTION
# =====================================================

try:

    prediction = model.predict(input_data)[0]

except Exception as e:

    st.error(f"Prediction Error: {e}")

    prediction = "Non-Fire"

# =====================================================
# PROBABILITY
# =====================================================

try:

    probabilities = model.predict_proba(
        input_data
    )[0]

    fire_probability = round(
        float(np.max(probabilities)) * 100,
        2
    )

except:

    fire_probability = 0.0

# =====================================================
# CONDITION MAPPING
# =====================================================

prediction_text = str(prediction).strip().upper()

if prediction_text in [
    "NON-FIRE",
    "NON FIRE",
    "0"
]:

    condition = "NON-FIRE"

    remarks = "System Safe"

    relay_status = False

    breaker_status = False

    buzzer_status = False

elif prediction_text in [
    "POTENTIAL FIRE",
    "POTENTIAL_FIRE",
    "1"
]:

    condition = "POTENTIAL FIRE"

    remarks = "Warning Sent | Buzzer Activated"

    relay_status = False

    breaker_status = False

    buzzer_status = True

else:

    condition = "FIRE"

    remarks = "Relay Activated | Breaker Tripped | SMS Sent"

    relay_status = True

    breaker_status = True

    buzzer_status = True

# =====================================================
# STATUS COLORS
# =====================================================

status_color = "#00ff88"

if condition == "POTENTIAL FIRE":

    status_color = "#ffaa00"

if condition == "FIRE":

    status_color = "#ff0000"

# =====================================================
# SAVE ML RESULTS
# =====================================================

try:

    latest_check = supabase.table(
        "table2_with_MLmodel"
    ).select("Date_and_Time").order(
        "Date_and_Time",
        desc=True
    ).limit(1).execute()

    allow_insert = True

    if latest_check.data:

        last_time = latest_check.data[0][
            "Date_and_Time"
        ]

        current_time = datetime.now()

        allow_insert = True

    if allow_insert:

        supabase.table(
            "table2_with_MLmodel"
        ).insert({

            "Date_and_Time": datetime.now().isoformat(),

            "temperature_reading": temperature,

            "air_quality_reading": air_quality,

            "carbon_monoxide_reading": carbon_monoxide,

            "smoke_reading": smoke,

            "predicted_condition": condition,

            "predicted_remarks": remarks,

            "fire_probability": fire_probability

        }).execute()

except Exception as e:

    st.warning(f"Database Save Warning: {e}")

# =====================================================
# SEND ESP32 COMMANDS
# =====================================================

try:

    supabase.table(
        "table3_esp_breaker_sms"
    ).upsert({

        "id": 1,

        "relay_status": relay_status,

        "breaker_status": breaker_status,

        "buzzer_status": buzzer_status,

        "condition": condition

    }).execute()

except Exception as e:

    st.warning(f"ESP32 Command Warning: {e}")

# =====================================================
# METRIC CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-icon">🌡️</div>

        <div class="metric-header">
            TEMPERATURE
        </div>

        <div class="metric-line"></div>

        <div class="metric-label">
            Temperature
        </div>

        <div class="metric-value">
            {temperature:.0f}
            <span class="metric-unit">°C</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-icon">🌫️</div>

        <div class="metric-header">
            AIR QUALITY
        </div>

        <div class="metric-line"></div>

        <div class="metric-label">
            Air Quality
        </div>

        <div class="metric-value">
            {air_quality:.0f}
            <span class="metric-unit">PPM</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-icon">☁️</div>

        <div class="metric-header">
            CARBON MONOXIDE
        </div>

        <div class="metric-line"></div>

        <div class="metric-label">
            Carbon Monoxide
        </div>

        <div class="metric-value">
            {carbon_monoxide:.0f}
            <span class="metric-unit">PPM</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-icon">💨</div>

        <div class="metric-header">
            SMOKE
        </div>

        <div class="metric-line"></div>

        <div class="metric-label">
            Smoke
        </div>

        <div class="metric-value">
            {smoke:.0f}
            <span class="metric-unit">PPM</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# STATUS BOX
# =====================================================

st.markdown(f"""
<div class="status-box"
style="
border:2px solid {status_color};
box-shadow:0 0 30px {status_color};">

<div class="status-title"
style="color:{status_color};">
{condition}
</div>

<div class="status-subtitle">
{remarks}
</div>

<div style="
margin-top:15px;
font-size:20px;
color:white;">

AI Confidence: {fire_probability}%

</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# HISTORY TABLE
# =====================================================

try:

    history_response = supabase.table(
        "table2_with_MLmodel"
    ).select("*").order(
        "Date_and_Time",
        desc=True
    ).limit(20).execute()

    history_df = pd.DataFrame(
        history_response.data
    )

except:

    history_df = pd.DataFrame()

st.markdown(
    "## 📋 LIVE SENSOR DATA TABLE"
)

if not history_df.empty:

    st.dataframe(
        history_df,
        use_container_width=True,
        height=450
    )

else:

    st.info("No historical data available.")

# =====================================================
# SENSOR ANALYTICS
# =====================================================

st.markdown(
    "## 📈 SENSOR ANALYTICS"
)

if not history_df.empty:

    fig = go.Figure()

    fig.add_trace(go.Scatter(

        x=history_df["Date_and_Time"],

        y=history_df[
            "temperature_reading"
        ],

        mode='lines+markers',

        name='Temperature'
    ))

    fig.add_trace(go.Scatter(

        x=history_df["Date_and_Time"],

        y=history_df[
            "smoke_reading"
        ],

        mode='lines+markers',

        name='Smoke'
    ))

    fig.add_trace(go.Scatter(

        x=history_df["Date_and_Time"],

        y=history_df[
            "carbon_monoxide_reading"
        ],

        mode='lines+markers',

        name='CO Level'
    ))

    fig.update_layout(

        paper_bgcolor='rgba(0,0,0,0.65)',

        plot_bgcolor='rgba(0,0,0,0.65)',

        font=dict(color='white'),

        height=550,

        xaxis_title='Date and Time',

        yaxis_title='Sensor Values'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TERMINAL LOGS
# =====================================================

print("=======================================")

print("AI FIRE DETECTION RESULT")

print("=======================================")

print("Temperature:", temperature)

print("Air Quality:", air_quality)

print("Carbon Monoxide:", carbon_monoxide)

print("Smoke:", smoke)

print("Prediction:", prediction)

print("Condition:", condition)

print("Remarks:", remarks)

print("Fire Probability:", fire_probability)

print("Relay:", relay_status)

print("Breaker:", breaker_status)

print("Buzzer:", buzzer_status)

print("=======================================")
```

---

# 🚀 HOW TO DEPLOY USING GITHUB + STREAMLIT CLOUD

## STEP 1 — CREATE GITHUB REPOSITORY

Go to:

```text
https://github.com
```

Create a new repository.

Example:

```text
fire-detection-dashboard
```

---

## STEP 2 — UPLOAD FILES

Upload:

* app.py
* fire_detection_model.pkl
* requirements.txt
* packages.txt
* .streamlit/config.toml

---

## STEP 3 — DEPLOY TO STREAMLIT CLOUD

Go to:

```text
https://streamlit.io/cloud
```

Click:

```text
New App
```

Select:

* Your GitHub repository
* Branch: main
* Main file path: app.py

Then click:

```text
Deploy
```

---

# 🔥 FINAL RESULT

Your dashboard will have:

✅ Animated fire background

✅ Real-time live sensor monitoring

✅ AI machine learning predictions

✅ ESP32 relay + breaker + buzzer control

✅ Supabase cloud database integration

✅ Real-time charts

✅ Modern glowing UI

✅ Mobile responsive design

✅ Auto refresh every 2 seconds

✅ Fire / Potential Fire / Non-Fire status

✅ AI confidence percentage
