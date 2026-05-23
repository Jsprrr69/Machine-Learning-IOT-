# =====================================================
# FIRE DETECTION AI DASHBOARD + ML + ESP32 CONTROL
# FIXED MACHINE LEARNING VERSION
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

    background:
    linear-gradient(
        180deg,
        rgba(25,25,25,0.95) 0%,
        rgba(10,10,10,0.95) 100%
    );

    border: 2px solid rgba(255,80,0,0.7);

    border-radius: 22px;

    padding: 35px;

    text-align: center;

    box-shadow:
        0px 0px 30px rgba(255,60,0,0.35);

    backdrop-filter: blur(10px);

    transition: 0.3s;

    min-height: 330px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.metric-box:hover {

    transform: translateY(-8px);

    box-shadow:
        0px 0px 45px rgba(255,80,0,0.7);
}

.metric-title {

    color: white;

    font-size: 28px;

    font-weight: bold;

    letter-spacing: 2px;

    margin-top: 10px;
}

.metric-value {

    color: #ff5e00;

    font-size: 60px;

    font-weight: bold;

    margin-top: 10px;

    text-shadow:
        0 0 10px rgba(255,80,0,0.7);
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
TABLE DESIGN
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

    overflow: hidden;

    position: relative;

    z-index: 999 !important;
}

h1, h2, h3 {

    color: white !important;
}

</style>

<div class="main-title">
FIRE DETECTION AND MONITORING SYSTEM
</div>

<div class="subtitle">
Live Sensor Readings
</div>

""", unsafe_allow_html=True)

# =====================================================
# FETCH RAW SENSOR DATA
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
# IMPORTANT:
# FEATURE ORDER MUST MATCH TRAINING
# =====================================================

input_data = pd.DataFrame([{
    'temperature': temperature,
    'air_quality': air_quality,
    'carbon_monoxide': carbon_monoxide,
    'smoke': smoke,
}])

# =====================================================
# MACHINE LEARNING PREDICTION
# =====================================================

prediction = model.predict(input_data)[0]

# =====================================================
# PREDICTION PROBABILITY
# =====================================================

try:

    probabilities = model.predict_proba(input_data)[0]

    fire_probability = float(np.max(probabilities))

except:

    fire_probability = 0.0

# =====================================================
# MACHINE LEARNING CONDITION MAPPING
# FIXED VERSION
# =====================================================

condition = str(prediction).strip()

# =====================================================
# NON-FIRE
# =====================================================

if (
    condition == "Non-Fire" or
    condition == "NON-FIRE" or
    condition == "0"
):

    condition = "NON-FIRE"

    remarks = "System Safe"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# POTENTIAL FIRE
# =====================================================

elif (
    condition == "Potential Fire" or
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
    condition == "Fire" or
    condition == "FIRE" or
    condition == "2"
):

    condition = "FIRE"

    remarks = "Relay Activated | Breaker Tripped | SMS Sent"

    relay_status = True

    breaker_status = True

    buzzer_status = True

# =====================================================
# UNKNOWN CONDITION
# =====================================================

else:

    condition = "UNKNOWN"

    remarks = "Model Returned Unknown Prediction"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# SAVE AI RESULTS TO SUPABASE
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

with col1:

    st.markdown(
        f"""
        <div class='metric-box'>

            <div style='
                font-size:55px;
                margin-bottom:10px;'>
                🌡
            </div>

            <div class='metric-title'>
                TEMPERATURE
            </div>

            <div style='
                color:white;
                font-size:22px;
                margin-top:20px;'>
                Temperature:
            </div>

            <div class='metric-value'>
                {temperature}°C
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class='metric-box'>

            <div style='
                font-size:55px;
                margin-bottom:10px;'>
                🌫
            </div>

            <div class='metric-title'>
                AIR QUALITY
            </div>

            <div style='
                color:white;
                font-size:22px;
                margin-top:20px;'>
                Air Quality:
            </div>

            <div class='metric-value'>
                {air_quality}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class='metric-box'>

            <div style='
                font-size:55px;
                margin-bottom:10px;'>
                ☠
            </div>

            <div class='metric-title'>
                CO LEVEL
            </div>

            <div style='
                color:white;
                font-size:22px;
                margin-top:20px;'>
                Carbon Monoxide:
            </div>

            <div class='metric-value'>
                {carbon_monoxide} PPM
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class='metric-box'>

            <div style='
                font-size:55px;
                margin-bottom:10px;'>
                💨
            </div>

            <div class='metric-title'>
                SMOKE
            </div>

            <div style='
                color:white;
                font-size:22px;
                margin-top:20px;'>
                Smoke:
            </div>

            <div class='metric-value'>
                {smoke} PPM
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
# =====================================================
# STATUS COLORS
# =====================================================

status_color = "#00ff99"

if condition == "POTENTIAL FIRE":

    status_color = "#ffaa00"

if condition == "FIRE":

    status_color = "#ff0000"

# =====================================================
# STATUS BOX
# =====================================================

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
