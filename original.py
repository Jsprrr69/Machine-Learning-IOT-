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
# CUSTOM UI DESIGN
# =====================================================
st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */
.stApp {
    background:
    linear-gradient(
        180deg,
        #000000 0%,
        #120000 30%,
        #220000 65%,
        #000000 100%
    );
    overflow: hidden;
}

/* =====================================================
MINIMALIST WAVY FIRE BACKGROUND
===================================================== */
.fire-wrapper {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 260px;
    z-index: -1;
    opacity: 0.35;
    overflow: hidden;
}

/* FIRE LAYERS */
.fire-wave {
    position: absolute;
    bottom: -40px;
    width: 200%;
    height: 240px;

    background:
        radial-gradient(circle at 50% 100%,
        rgba(255,140,0,0.95) 0%,
        rgba(255,69,0,0.75) 25%,
        rgba(255,0,0,0.45) 45%,
        transparent 70%);

    border-radius: 45%;

    filter: blur(35px);

    animation: waveFire 6s ease-in-out infinite;
}

/* SECOND FIRE */
.fire-wave2 {
    animation-delay: 2s;
    opacity: 0.5;
    height: 280px;
}

/* THIRD FIRE */
.fire-wave3 {
    animation-delay: 4s;
    opacity: 0.3;
    height: 220px;
}

/* WAVE ANIMATION */
@keyframes waveFire {

    0% {
        transform:
            translateX(-10%)
            translateY(0px)
            scaleY(1);
    }

    25% {
        transform:
            translateX(-5%)
            translateY(-15px)
            scaleY(1.08);
    }

    50% {
        transform:
            translateX(0%)
            translateY(-25px)
            scaleY(1.15);
    }

    75% {
        transform:
            translateX(5%)
            translateY(-10px)
            scaleY(1.05);
    }

    100% {
        transform:
            translateX(10%)
            translateY(0px)
            scaleY(1);
    }
}

/* =====================================================
GLOWING EMBERS
===================================================== */
.embers {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
}

.embers span {
    position: absolute;
    bottom: -20px;
    width: 4px;
    height: 4px;
    background: orange;
    border-radius: 50%;
    box-shadow: 0 0 10px orange;
    animation: emberFloat linear infinite;
}

.embers span:nth-child(1) {
    left: 10%;
    animation-duration: 7s;
}

.embers span:nth-child(2) {
    left: 25%;
    animation-duration: 9s;
}

.embers span:nth-child(3) {
    left: 40%;
    animation-duration: 6s;
}

.embers span:nth-child(4) {
    left: 55%;
    animation-duration: 10s;
}

.embers span:nth-child(5) {
    left: 70%;
    animation-duration: 8s;
}

.embers span:nth-child(6) {
    left: 85%;
    animation-duration: 11s;
}

@keyframes emberFloat {

    0% {
        transform: translateY(0px) scale(1);
        opacity: 0;
    }

    20% {
        opacity: 1;
    }

    100% {
        transform: translateY(-100vh) scale(0);
        opacity: 0;
    }
}

/* =====================================================
TITLE
===================================================== */
.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: bold;
    color: white;
    text-shadow:
        0 0 10px red,
        0 0 20px red,
        0 0 40px orange;
}

.subtitle {
    text-align: center;
    color: #cccccc;
    font-size: 20px;
    margin-bottom: 30px;
}

/* =====================================================
METRIC BOXES
===================================================== */
.metric-box {
    background: rgba(0,0,0,0.65);
    border: 1px solid rgba(255,0,0,0.6);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(255,0,0,0.3);
}

.metric-title {
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.metric-value {
    color: #ff4b4b;
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
    box-shadow: 0px 0px 20px red;
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

<!-- =====================================================
MINIMALIST FIRE HTML
===================================================== -->

<div class="fire-wrapper">
    <div class="fire-wave"></div>
    <div class="fire-wave fire-wave2"></div>
    <div class="fire-wave fire-wave3"></div>
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

        temp = random.randint(30, 65)
        air = random.randint(500, 2500)
        smoke = random.randint(400, 3200)
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
<div class="status-box" style="border-color:{status_color}; box-shadow:0px 0px 30px {status_color};">
<div class="status-text" style="color:{status_color};">
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
