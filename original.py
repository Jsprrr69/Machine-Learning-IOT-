# =====================================================
# FIRE DETECTION AI DASHBOARD + ML + ESP32 CONTROL
# =====================================================

# =====================================================
# INSTALL REQUIRED LIBRARIES
# =====================================================
#
# pip install streamlit pandas numpy
# pip install scikit-learn supabase
# pip install joblib plotly
#
# =====================================================
# =====================================================
# FILE NAME:
# predict_and_control.py
#
# PURPOSE:
# 1. Get RAW sensor data from Supabase
# 2. Run Machine Learning prediction
# 3. Save prediction results to Supabase
# 4. Notify ESP32 to activate:
#       - Relay
#       - Breaker
#       - Buzzer
# 5. Dashboard reads FINAL AI results
#
# ======================================================

# =====================================================
# INSTALL REQUIRED LIBRARIES
# =====================================================
#
# pip install pandas numpy scikit-learn
# pip install supabase joblib
#
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import time

from supabase import create_client
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fire Detection Dashboard",
    layout="wide"
)

# =====================================================
# SUPABASE CONFIGURATION
# =====================================================
# CHANGE THESE
# =====================================================

SUPABASE_URL = "https://cofxcqxbiminjabrptrp.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNvZnhjcXhiaW1pbmphYnJwdHJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1ODEyMDAsImV4cCI6MjA5MjE1NzIwMH0.6FDwnj_AiaOPVoYNiRA43RKDn3cqLYK00rTHuSaNh3c"

# =====================================================
# CONNECT TO SUPABASE
# =====================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================================
# LOAD MACHINE LEARNING MODEL
# =====================================================
# CHANGE THIS IF YOUR FILE NAME IS DIFFERENT
# =====================================================

model = joblib.load("fire_detection_model.pkl")

# =====================================================
# FIRE BACKGROUND CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
APP BACKGROUND
===================================================== */
.stApp {

    background:
    radial-gradient(circle at center,
    #250000 0%,
    #0a0000 45%,
    #000000 100%);

    overflow-x: hidden;
}

/* =====================================================
FIRE LAYER
===================================================== */
.stApp::before {

    content: "";

    position: fixed;

    bottom: -120px;
    left: -10%;

    width: 120%;
    height: 420px;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,220,120,0.95) 0%,
        rgba(255,140,0,0.85) 20%,
        rgba(255,60,0,0.55) 45%,
        rgba(255,0,0,0.18) 70%,
        transparent 85%
    );

    filter: blur(55px);

    animation:
        fireWave1 7s ease-in-out infinite;

    z-index: 0;

    pointer-events: none;
}

.stApp::after {

    content: "";

    position: fixed;

    bottom: -160px;
    left: -15%;

    width: 130%;
    height: 520px;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,180,0,0.75) 0%,
        rgba(255,80,0,0.45) 40%,
        transparent 80%
    );

    filter: blur(90px);

    animation:
        fireWave2 10s ease-in-out infinite;

    z-index: 0;

    pointer-events: none;
}

/* =====================================================
ANIMATION
===================================================== */
@keyframes fireWave1 {

    0% {
        transform:
            translateX(-3%)
            translateY(0px)
            scaleY(1);
    }

    25% {
        transform:
            translateX(0%)
            translateY(-30px)
            scaleY(1.15);
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
            translateY(-25px)
            scaleY(1.1);
    }

    100% {
        transform:
            translateX(-3%)
            translateY(0px)
            scaleY(1);
    }
}

@keyframes fireWave2 {

    0% {
        transform:
            translateX(0%)
            scale(1);
    }

    50% {
        transform:
            translateX(-2%)
            scale(1.08);
    }

    100% {
        transform:
            translateX(0%)
            scale(1);
    }
}

/* =====================================================
MAIN CONTENT
===================================================== */
.main .block-container {

    position: relative;

    z-index: 5;
}

/* =====================================================
TITLE
===================================================== */
.main-title {

    text-align: center;

    font-size: 60px;

    font-weight: bold;

    color: white;

    text-shadow:
        0 0 10px red,
        0 0 20px red,
        0 0 40px orange;

    margin-bottom: 10px;
}

.subtitle {

    text-align: center;

    color: #dddddd;

    font-size: 20px;

    margin-bottom: 30px;
}

/* =====================================================
METRIC BOXES
===================================================== */
.metric-box {

    background: rgba(0,0,0,0.72);

    border: 1px solid rgba(255,80,0,0.5);

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    box-shadow:
        0px 0px 20px rgba(255,0,0,0.3);

    backdrop-filter: blur(6px);

    position: relative;

    z-index: 5;
}

.metric-title {

    color: white;

    font-size: 18px;

    font-weight: bold;
}

.metric-value {

    color: #ff7b42;

    font-size: 38px;

    font-weight: bold;
}

/* =====================================================
STATUS BOX
===================================================== */
.status-box {

    background: rgba(0,0,0,0.75);

    border-radius: 20px;

    padding: 20px;

    text-align: center;

    margin-top: 20px;
    margin-bottom: 20px;

    border: 2px solid red;

    box-shadow:
        0px 0px 25px red;

    backdrop-filter: blur(5px);

    position: relative;

    z-index: 5;
}

.status-text {

    font-size: 38px;

    font-weight: bold;
}

/* =====================================================
RED TABLE DESIGN
===================================================== */

[data-testid="stDataFrame"] {

    background:
    linear-gradient(
        180deg,
        rgba(45,0,0,0.96) 0%,
        rgba(15,0,0,0.96) 100%
    ) !important;

    border: 2px solid rgba(255,80,0,0.8);

    border-radius: 15px;

    box-shadow:
        0 0 25px rgba(255,60,0,0.25);

    overflow: hidden;

    position: relative;

    z-index: 999 !important;
}

[data-testid="stDataFrame"] [role="grid"] {

    background-color:
    rgba(25,0,0,0.95) !important;

    color: white !important;
}

[data-testid="stDataFrame"] [role="columnheader"] {

    background:
    linear-gradient(
        180deg,
        rgba(120,0,0,1) 0%,
        rgba(70,0,0,1) 100%
    ) !important;

    color: white !important;

    font-weight: bold !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {

    background-color:
    rgba(30,0,0,0.92) !important;

    color: white !important;
}

[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] {

    background-color:
    rgba(255,60,0,0.20) !important;
}

/* =====================================================
HEADERS
===================================================== */
h1, h2, h3 {

    color: white !important;
}

</style>

<div class="main-title">
🔥 LIVE SENSOR READINGS
</div>

<div class="subtitle">
AI Fire Detection and Monitoring System
</div>

""", unsafe_allow_html=True)

# =====================================================
# FETCH LATEST RAW SENSOR DATA
# =====================================================
#
# TABLE:
# raw_sensor_readings
#
# =====================================================

response = supabase.table(
    "table1_raw_data"
).select("*").order(
    "Date_and_Time",
    desc=True
).limit(1).execute()

# =====================================================
# CHECK IF EMPTY
# =====================================================

if len(response.data) == 0:

    st.warning("No sensor data found.")

    st.stop()

# =====================================================
# CONVERT TO DATAFRAME
# =====================================================

df = pd.DataFrame(response.data)

latest = df.iloc[0]

# =====================================================
# GET SENSOR VALUES
# =====================================================

temperature = latest["temperature_reading"]

air_quality = latest["air_quality_reading"]

carbon_monoxide = latest["carbon_monoxide_reading"]

smoke = latest["smoke_reading"]



# =====================================================
# PREPARE ML INPUT
# =====================================================

X = np.array([[
    temperature,
    air_quality,
    carbon_monoxide,
    smoke
   
]])

# =====================================================
# MACHINE LEARNING PREDICTION
# =====================================================

prediction = model.predict(X)[0]

# =====================================================
# PREDICTION PROBABILITY
# =====================================================

try:

    probabilities = model.predict_proba(X)[0]

    fire_probability = float(np.max(probabilities))

except:

    fire_probability = 0.0

# =====================================================
# MACHINE LEARNING CONDITION MAPPING
# =====================================================

condition = str(prediction).upper()

# =====================================================
# NORMAL
# =====================================================

if (
    condition == "NORMAL" or
    condition == "0"
):

    condition = "NORMAL"

    remarks = "System Safe"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# POTENTIAL FIRE
# =====================================================

elif (
    condition == "POTENTIAL FIRE" or
    condition == "POTENTIAL_FIRE" or
    condition == "1"
):

    condition = "POTENTIAL FIRE"

    remarks = "Warning Sent | Buzzer Activated"

    relay_status = False

    breaker_status = False

    buzzer_status = True

# =====================================================
# FIRE
# =====================================================

elif (
    condition == "FIRE" or
    condition == "2"
):

    condition = "FIRE"

    remarks = "Relay Activated | Breaker Tripped | SMS Sent"

    relay_status = True

    breaker_status = True

    buzzer_status = True

# =====================================================
# UNKNOWN
# =====================================================

else:

    condition = "UNKNOWN"

    remarks = "Unknown Prediction"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# SAVE AI RESULTS TO SUPABASE
# =====================================================
#
# TABLE:
# predicted_sensor_readings
#
# =====================================================

supabase.table(
    "table2_with_MLmodel"
).insert({

    "Date_and_Time":
    datetime.now().isoformat(),

    "temperature_reading":
    float(temperature),

    "air_quality_reading":
    int(air_quality),

    "carbon_monoxide_reading":
    int(carbon_monoxide),
    
    "smoke_reading":
    int(smoke),

    "predicted_condition":
    condition,

    "predicted_remarks":
    remarks,

    "fire_probability":
    fire_probability

}).execute()

# =====================================================
# SEND CONTROL COMMANDS TO ESP32
# =====================================================
#
# TABLE:
# esp32_control
#
# =====================================================

supabase.table(
    "table3_esp_breaker_sms"
).upsert({

    "id": 1,

    "relay_status":
    relay_status,

    "breaker_status":
    breaker_status,

    "buzzer_status":
    buzzer_status,

    "condition":
    condition

}).execute()

# =====================================================
# METRIC BOXES
# =====================================================

col1, col2, col3, col4 = st.columns(4)

metrics = [

    ("🌡 TEMPERATURE",
     f"{temperature}°C"),

    ("🌫 AIR QUALITY",
     air_quality),

    ("☠ CO LEVEL",
     carbon_monoxide),

    ("💨 SMOKE",
     smoke)
]

for col, metric in zip(
    [col1, col2, col3, col4],
    metrics
):

    with col:

        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-title">
                {metric[0]}
            </div>

            <div class="metric-value">
                {metric[1]}
            </div>
        </div>
        ''', unsafe_allow_html=True)

# =====================================================
# STATUS BOX
# =====================================================

status_color = "#00ff99"

if condition == "POTENTIAL FIRE":

    status_color = "#ffaa00"

if condition == "FIRE":

    status_color = "#ff0000"

st.markdown(f'''
<div class="status-box"
style="border-color:{status_color};
box-shadow:0px 0px 30px {status_color};">

<div class="status-text"
style="color:{status_color};">

{condition}

</div>

<div style="
color:white;
margin-top:10px;
font-size:18px;">

{remarks}

</div>

</div>
''', unsafe_allow_html=True)

# =====================================================
# HISTORY TABLE
# =====================================================

history_response = supabase.table(
    "table2_with_MLmodel"
).select("*").order(
    "Date_and_Time",
    desc=True
).limit(15).execute()

history_df = pd.DataFrame(
    history_response.data
)

st.markdown(
    "## 📋 LIVE SENSOR DATA TABLE"
)

st.dataframe(
    history_df,
    use_container_width=True,
    height=500
)

# =====================================================
# CHART
# =====================================================

st.markdown(
    "## 📈 SENSOR ANALYTICS"
)

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

    paper_bgcolor=
    'rgba(0,0,0,0.6)',

    plot_bgcolor=
    'rgba(0,0,0,0.6)',

    font=dict(color='white'),

    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TERMINAL OUTPUT
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

# =====================================================
# AUTO REFRESH
# =====================================================

time.sleep(2)

st.rerun()
