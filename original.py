import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="🔥 Fire Detection Dashboard",
    layout="wide"
)

# =====================================================
# LIVE FIRE UI DESIGN
# =====================================================
st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */
.stApp {
    background:
    radial-gradient(circle at center,
    #220000 0%,
    #0a0000 50%,
    #000000 100%);
}

/* =====================================================
FIRE CONTAINER
===================================================== */
.live-fire-container {
    position: fixed;
    bottom: 0;
    left: 0;

    width: 100%;
    height: 420px;

    overflow: hidden;

    z-index: -1;

    pointer-events: none;
}

/* =====================================================
FIRE GLOW
===================================================== */
.fire-glow {

    position: absolute;

    bottom: -120px;
    left: -20%;

    width: 140%;
    height: 350px;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,120,0,0.9) 0%,
        rgba(255,60,0,0.7) 30%,
        rgba(255,0,0,0.4) 55%,
        transparent 75%
    );

    filter: blur(60px);

    animation: firePulse 5s ease-in-out infinite;
}

/* =====================================================
FIRE WAVES
===================================================== */
.fire-wave {

    position: absolute;

    bottom: -100px;
    left: -20%;

    width: 150%;
    height: 300px;

    border-radius: 45%;

    background:
    radial-gradient(
        ellipse at center,
        rgba(255,200,0,0.95) 0%,
        rgba(255,120,0,0.8) 20%,
        rgba(255,0,0,0.55) 45%,
        rgba(255,0,0,0.1) 70%,
        transparent 85%
    );

    filter: blur(40px);

    mix-blend-mode: screen;

    animation:
        fireWave 7s ease-in-out infinite;
}

/* SECOND FIRE */
.wave2 {
    animation-delay: 2s;
    opacity: 0.7;
    height: 360px;
}

/* THIRD FIRE */
.wave3 {
    animation-delay: 4s;
    opacity: 0.5;
    height: 240px;
}

/* =====================================================
FIRE MOVEMENT
===================================================== */
@keyframes fireWave {

    0% {
        transform:
            translateX(-5%)
            translateY(0px)
            scaleY(1);
    }

    25% {
        transform:
            translateX(0%)
            translateY(-25px)
            scaleY(1.15);
    }

    50% {
        transform:
            translateX(5%)
            translateY(-50px)
            scaleY(1.35);
    }

    75% {
        transform:
            translateX(0%)
            translateY(-20px)
            scaleY(1.1);
    }

    100% {
        transform:
            translateX(-5%)
            translateY(0px)
            scaleY(1);
    }
}

/* =====================================================
FIRE GLOW ANIMATION
===================================================== */
@keyframes firePulse {

    0% {
        opacity: 0.7;
        transform: scale(1);
    }

    50% {
        opacity: 1;
        transform: scale(1.08);
    }

    100% {
        opacity: 0.7;
        transform: scale(1);
    }
}

/* =====================================================
EMBERS
===================================================== */
.embers {

    position: fixed;

    inset: 0;

    z-index: -1;

    pointer-events: none;
}

.embers span {

    position: absolute;

    bottom: -20px;

    width: 6px;
    height: 6px;

    border-radius: 50%;

    background:
    radial-gradient(circle,
    #fff3b0 0%,
    orange 50%,
    red 100%);

    box-shadow:
        0 0 10px orange,
        0 0 20px red;

    animation:
        emberRise linear infinite;
}

/* RANDOM EMBERS */
.embers span:nth-child(1) {
    left: 10%;
    animation-duration: 8s;
}

.embers span:nth-child(2) {
    left: 25%;
    animation-duration: 11s;
}

.embers span:nth-child(3) {
    left: 40%;
    animation-duration: 7s;
}

.embers span:nth-child(4) {
    left: 55%;
    animation-duration: 13s;
}

.embers span:nth-child(5) {
    left: 70%;
    animation-duration: 9s;
}

.embers span:nth-child(6) {
    left: 85%;
    animation-duration: 10s;
}

/* =====================================================
EMBER MOVEMENT
===================================================== */
@keyframes emberRise {

    0% {

        transform:
            translateY(0px)
            scale(1);

        opacity: 0;
    }

    15% {
        opacity: 1;
    }

    100% {

        transform:
            translateY(-100vh)
            translateX(60px)
            scale(0);

        opacity: 0;
    }
}

/* =====================================================
CONTENT ABOVE FIRE
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

    background: rgba(0,0,0,0.70);

    border: 1px solid rgba(255,80,0,0.5);

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    box-shadow:
        0px 0px 20px rgba(255,0,0,0.3);
}

.metric-title {
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.metric-value {
    color: #ff5c33;
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
}

.status-text {
    font-size: 38px;
    font-weight: bold;
}

/* =====================================================
TABLE
===================================================== */
[data-testid="stDataFrame"] {

    background-color: rgba(0,0,0,0.65);

    border-radius: 15px;

    border: 1px solid red;

    padding: 10px;
}

/* =====================================================
PLOTLY CHART
===================================================== */
.js-plotly-plot {
    border-radius: 20px;
    overflow: hidden;
}

</style>

<div class="live-fire-container">

    <div class="fire-glow"></div>

    <div class="fire-wave"></div>

    <div class="fire-wave wave2"></div>

    <div class="fire-wave wave3"></div>

</div>

<div class="embers">

    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>

</div>

<div class="main-title">
🔥 LIVE SENSOR READINGS
</div>

<div class="subtitle">
Fire Detection and Monitoring System
</div>

""", unsafe_allow_html=True)

# =====================================================
# MOCK DATA STORAGE
# =====================================================
if "sensor_data" not in st.session_state:

    rows = []

    for i in range(12):

        temp = random.randint(30, 70)
        air = random.randint(500, 2500)
        smoke = random.randint(400, 3500)
        co = random.randint(300, 2500)

        condition = "NORMAL"
        remarks = "Safe"

        if smoke > 2500 or co > 2200 or temp > 55:
            condition = "FIRE"
            remarks = "Breaker tripped & SMS sent"

        elif smoke > 1700 or co > 1500 or temp > 45:
            condition = "POTENTIAL FIRE"
            remarks = "SMS Sent"

        rows.append({
            "Time": datetime.now().strftime("%I:%M:%S %p"),
            "Temperature Reading (°C)": temp,
            "Air Quality Reading": air,
            "Smoke Reading": smoke,
            "Carbon Monoxide Reading": co,
            "Condition": condition,
            "Remarks": remarks
        })

    st.session_state.sensor_data = pd.DataFrame(rows)

# =====================================================
# ADD NEW MOCK READING
# =====================================================
new_temp = random.randint(30, 70)
new_air = random.randint(500, 2600)
new_smoke = random.randint(400, 3500)
new_co = random.randint(300, 2700)

condition = "NORMAL"
remarks = "Safe"

if new_smoke > 2600 or new_co > 2300 or new_temp > 60:
    condition = "FIRE"
    remarks = "Breaker tripped & SMS sent"

elif new_smoke > 1800 or new_co > 1600 or new_temp > 48:
    condition = "POTENTIAL FIRE"
    remarks = "SMS Sent"

new_row = pd.DataFrame([{
    "Time": datetime.now().strftime("%I:%M:%S %p"),
    "Temperature Reading (°C)": new_temp,
    "Air Quality Reading": new_air,
    "Smoke Reading": new_smoke,
    "Carbon Monoxide Reading": new_co,
    "Condition": condition,
    "Remarks": remarks
}])

st.session_state.sensor_data = pd.concat([
    new_row,
    st.session_state.sensor_data
]).head(15)

df = st.session_state.sensor_data

# =====================================================
# LATEST VALUES
# =====================================================
latest = df.iloc[0]

# =====================================================
# METRICS
# =====================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">🌡 TEMPERATURE</div>
        <div class="metric-value">{latest['Temperature Reading (°C)']}°C</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">🌫 AIR QUALITY</div>
        <div class="metric-value">{latest['Air Quality Reading']}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">💨 SMOKE</div>
        <div class="metric-value">{latest['Smoke Reading']}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">☠ CO LEVEL</div>
        <div class="metric-value">{latest['Carbon Monoxide Reading']}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# STATUS DISPLAY
# =====================================================
status = latest["Condition"]

status_color = "#00ff99"

if status == "POTENTIAL FIRE":
    status_color = "#ffaa00"

if status == "FIRE":
    status_color = "#ff0000"

st.markdown(f"""
<div class="status-box"
style="border-color:{status_color};
box-shadow:0px 0px 30px {status_color};">

<div class="status-text"
style="color:{status_color};">

{status}

</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SENSOR TABLE
# =====================================================
st.markdown("## 📋 LIVE SENSOR DATA TABLE")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# =====================================================
# CHARTS
# =====================================================
st.markdown("## 📈 SENSOR ANALYTICS")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Temperature Reading (°C)"],
    mode='lines+markers',
    name='Temperature'
))

fig.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Smoke Reading"],
    mode='lines+markers',
    name='Smoke'
))

fig.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Carbon Monoxide Reading"],
    mode='lines+markers',
    name='Carbon Monoxide'
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0.6)',
    plot_bgcolor='rgba(0,0,0,0.6)',
    font=dict(color='white'),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# AUTO REFRESH
# =====================================================
time.sleep(2)
st.rerun()
