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
RED TABLE DESIGN FIX
===================================================== */

/* OUTER TABLE CONTAINER */
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

/* MAIN GRID AREA */
[data-testid="stDataFrame"] [role="grid"] {

    background-color:
    rgba(25,0,0,0.95) !important;

    color: white !important;
}

/* COLUMN HEADERS */
[data-testid="stDataFrame"] [role="columnheader"] {

    background:
    linear-gradient(
        180deg,
        rgba(120,0,0,1) 0%,
        rgba(70,0,0,1) 100%
    ) !important;

    color: white !important;

    font-weight: bold !important;

    border-color:
    rgba(255,120,0,0.35) !important;
}

/* TABLE CELLS */
[data-testid="stDataFrame"] [role="gridcell"] {

    background-color:
    rgba(30,0,0,0.92) !important;

    color: white !important;

    border-color:
    rgba(255,80,0,0.15) !important;
}

/* ROW HOVER EFFECT */
[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] {

    background-color:
    rgba(255,60,0,0.20) !important;
}

/* SCROLL AREA */
[data-testid="stDataFrame"] div {

    color: white !important;
}

/* =====================================================
CHART
===================================================== */
.js-plotly-plot {

    position: relative;

    z-index: 5;
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
