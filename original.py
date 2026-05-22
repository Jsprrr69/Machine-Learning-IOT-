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
# UI DESIGN
# =====================================================
st.markdown("""
<style>

/* =====================================================
MAIN APP BACKGROUND
===================================================== */
.stApp {

    background:
    radial-gradient(circle at top,
    #2b0000 0%,
    #120000 35%,
    #050505 75%,
    #000000 100%);

    overflow-x: hidden;
}

/* =====================================================
KEEP CONTENT ABOVE ANIMATION
===================================================== */
.main .block-container {

    position: relative;
    z-index: 10;
}

/* =====================================================
FIRE BACKGROUND LAYER
===================================================== */
.fire-bg {

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    z-index: 0;

    pointer-events: none;
}

/* =====================================================
MAIN FIRE WAVES
===================================================== */
.fire-wave1,
.fire-wave2,
.fire-wave3 {

    position: absolute;

    bottom: -250px;

    width: 140%;
    height: 700px;

    border-radius: 40%;

    filter: blur(70px);

    opacity: 0.55;
}

/* =====================================================
WAVE 1
===================================================== */
.fire-wave1 {

    left: -20%;

    background:
    radial-gradient(circle,
    rgba(255,220,120,0.95) 0%,
    rgba(255,140,0,0.😎 20%,
    rgba(255,70,0,0.55) 45%,
    rgba(255,0,0,0.12) 75%,
    transparent 90%);

    animation:
    waveMove1 8s ease-in-out infinite;
}

/* =====================================================
WAVE 2
===================================================== */
.fire-wave2 {

    left: -10%;

    background:
    radial-gradient(circle,
    rgba(255,180,0,0.😎 0%,
    rgba(255,80,0,0.5) 40%,
    rgba(255,0,0,0.15) 70%,
    transparent 85%);

    animation:
    waveMove2 11s ease-in-out infinite;
}

/* =====================================================
WAVE 3
===================================================== */
.fire-wave3 {

    left: -15%;

    background:
    radial-gradient(circle,
    rgba(255,255,255,0.2) 0%,
    rgba(255,160,0,0.3) 20%,
    rgba(255,60,0,0.2) 50%,
    transparent 80%);

    animation:
    waveMove3 14s ease-in-out infinite;
}

/* =====================================================
FIRE PARTICLES / EMBERS
===================================================== */
.fire-particle {

    position: absolute;

    bottom: -20px;

    width: 8px;
    height: 8px;

    background: orange;

    border-radius: 50%;

    box-shadow:
    0 0 10px orange,
    0 0 20px red;

    opacity: 0.7;

    animation:
    emberFloat linear infinite;
}

/* =====================================================
EMBER POSITIONS
===================================================== */
.fire-particle:nth-child(1) {
    left: 10%;
    animation-duration: 8s;
    animation-delay: 0s;
}

.fire-particle:nth-child(2) {
    left: 25%;
    animation-duration: 10s;
    animation-delay: 2s;
}

.fire-particle:nth-child(3) {
    left: 40%;
    animation-duration: 7s;
    animation-delay: 1s;
}

.fire-particle:nth-child(4) {
    left: 55%;
    animation-duration: 9s;
    animation-delay: 3s;
}

.fire-particle:nth-child(5) {
    left: 70%;
    animation-duration: 12s;
    animation-delay: 2s;
}

.fire-particle:nth-child(6) {
    left: 85%;
    animation-duration: 8s;
    animation-delay: 4s;
}

/* =====================================================
ANIMATIONS
===================================================== */
@keyframes waveMove1 {

    0% {
        transform:
        translateX(0%)
        translateY(0px)
        scaleY(1);
    }

    50% {
        transform:
        translateX(-3%)
        translateY(-80px)
        scaleY(1.2);
    }

    100% {
        transform:
        translateX(0%)
        translateY(0px)
        scaleY(1);
    }
}

@keyframes waveMove2 {

    0% {
        transform:
        translateX(0%)
        scale(1);
    }

    50% {
        transform:
        translateX(2%)
        scale(1.08);
    }

    100% {
        transform:
        translateX(0%)
        scale(1);
    }
}

@keyframes waveMove3 {

    0% {
        transform:
        translateX(0%)
        translateY(0px);
    }

    50% {
        transform:
        translateX(-2%)
        translateY(-40px);
    }

    100% {
        transform:
        translateX(0%)
        translateY(0px);
    }
}

@keyframes emberFloat {

    0% {

        transform:
        translateY(0px)
        translateX(0px)
        scale(1);

        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    50% {

        transform:
        translateY(-400px)
        translateX(20px)
        scale(1.5);
    }

    100% {

        transform:
        translateY(-850px)
        translateX(-20px)
        scale(0.5);

        opacity: 0;
    }
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

    backdrop-filter: blur(8px);
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

    backdrop-filter: blur(8px);
}

.status-text {

    font-size: 38px;

    font-weight: bold;
}

/* =====================================================
TABLE
===================================================== */
[data-testid="stDataFrame"] {

    background-color: rgba(0,0,0,0.78);

    border-radius: 15px;

    border: 1px solid red;

    padding: 10px;

    backdrop-filter: blur(10px);

    position: relative;

    z-index: 20;
}

/* =====================================================
PLOTLY CHART
===================================================== */
.js-plotly-plot {

    position: relative;

    z-index: 20;
}

</style>

<div class="fire-bg">

    <div class="fire-wave1"></div>
    <div class="fire-wave2"></div>
    <div class="fire-wave3"></div>

    <div class="fire-particle"></div>
    <div class="fire-particle"></div>
    <div class="fire-particle"></div>
    <div class="fire-particle"></div>
    <div class="fire-particle"></div>
    <div class="fire-particle"></div>

</div>

<div class="main-title">
🔥 LIVE SENSOR READINGS
</div>

<div class="subtitle">
Fire Detection and Monitoring System
</div>

""", unsafe_allow_html=True)

# =====================================================
# MOCK DATA
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
# NEW DATA
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

latest = df.iloc[0]

# =====================================================
# METRICS
# =====================================================
col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("🌡 TEMPERATURE", f"{latest['Temperature Reading (°C)']}°C"),
    ("🌫 AIR QUALITY", latest["Air Quality Reading"]),
    ("💨 SMOKE", latest["Smoke Reading"]),
    ("☠ CO LEVEL", latest["Carbon Monoxide Reading"])
]

for col, metric in zip([col1, col2, col3, col4], metrics):

    with col:

        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-title">{metric[0]}</div>
            <div class="metric-value">{metric[1]}</div>
        </div>
        ''', unsafe_allow_html=True)

# =====================================================
# STATUS
# =====================================================
status = latest["Condition"]

status_color = "#00ff99"

if status == "POTENTIAL FIRE":
    status_color = "#ffaa00"

if status == "FIRE":
    status_color = "#ff0000"

st.markdown(f'''
<div class="status-box"
style="border-color:{status_color};
box-shadow:0px 0px 30px {status_color};">

<div class="status-text"
style="color:{status_color};">

{status}

</div>
</div>
''', unsafe_allow_html=True)

# =====================================================
# TABLE
# =====================================================
st.markdown("## 📋 LIVE SENSOR DATA TABLE")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# =====================================================
# CHART
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
    name='CO Level'
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
