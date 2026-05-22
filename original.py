import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="🔥 Fire Detection Dashboard",
    layout="wide"
)

# ======================================================
# CUSTOM CSS DESIGN
# ======================================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #2b0000, #000000);
    overflow: hidden;
}

/* FIRE ANIMATION BACKGROUND */
.fire-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0.15;
    background: radial-gradient(circle at 50% 100%,
        rgba(255,80,0,0.8),
        rgba(255,0,0,0.4),
        transparent 70%);
    animation: firemove 3s infinite alternate;
}

@keyframes firemove {
    0% {
        transform: scale(1) translateY(0px);
        filter: blur(20px);
    }

    50% {
        transform: scale(1.1) translateY(-20px);
        filter: blur(30px);
    }

    100% {
        transform: scale(1.05) translateY(-10px);
        filter: blur(25px);
    }
}

/* TITLE */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #ff4b4b;
    text-shadow: 0px 0px 20px red;
}

/* STATUS BOX */
.status-box {
    background-color: rgba(0,0,0,0.6);
    border: 2px solid red;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    box-shadow: 0px 0px 20px red;
}

/* TABLE */
table {
    color: white !important;
}

thead tr th {
    background-color: rgba(255,0,0,0.8) !important;
    color: white !important;
    font-size: 18px !important;
    text-align: center !important;
}

tbody tr {
    background-color: rgba(0,0,0,0.65) !important;
}

tbody td {
    color: white !important;
    font-size: 16px !important;
    text-align: center !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: rgba(0,0,0,0.65);
    border: 2px solid red;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px red;
}

[data-testid="metric-container"] label {
    color: white !important;
}

[data-testid="metric-container"] div {
    color: #ff4b4b !important;
}

/* CHARTS */
.js-plotly-plot {
    background-color: rgba(0,0,0,0.5) !important;
    border-radius: 15px;
    padding: 10px;
}

</style>

<div class="fire-bg"></div>

<div class="title">
🔥 FIRE DETECTION DASHBOARD 🔥
</div>
""", unsafe_allow_html=True)

# ======================================================
# MOCK LIVE DATA
# ======================================================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Time",
        "Temperature Reading",
        "Air Quality Reading",
        "Smoke Reading",
        "Carbon Monoxide Reading"
    ])

# ======================================================
# GENERATE MOCK SENSOR VALUES
# ======================================================
def generate_data():
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Temperature Reading": random.randint(28, 75),
        "Air Quality Reading": random.randint(400, 2500),
        "Smoke Reading": random.randint(300, 3500),
        "Carbon Monoxide Reading": random.randint(200, 3000)
    }

# ======================================================
# ADD NEW DATA
# ======================================================
new_row = generate_data()

st.session_state.data = pd.concat([
    st.session_state.data,
    pd.DataFrame([new_row])
], ignore_index=True)

# Keep only latest 20 rows
st.session_state.data = st.session_state.data.tail(20)

df = st.session_state.data

# ======================================================
# FIRE CONDITION
# ======================================================
latest = df.iloc[-1]

temp = latest["Temperature Reading"]
air = latest["Air Quality Reading"]
smoke = latest["Smoke Reading"]
co = latest["Carbon Monoxide Reading"]

condition = "✅ SAFE"
color = "#00ff88"

if temp > 55 or smoke > 2500 or co > 2200:
    condition = "🔥 FIRE DETECTED"
    color = "#ff0000"

elif temp > 45 or smoke > 1800 or co > 1500:
    condition = "⚠ WARNING"
    color = "#ffaa00"

# ======================================================
# STATUS DISPLAY
# ======================================================
st.markdown(f"""
<div class="status-box" style="border-color:{color}; box-shadow:0px 0px 20px {color};">
{condition}
</div>
""", unsafe_allow_html=True)

# ======================================================
# LIVE METRICS
# ======================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Temperature", f"{temp} °C")
col2.metric("🌫 Air Quality", air)
col3.metric("💨 Smoke", smoke)
col4.metric("☠ Carbon Monoxide", co)

# ======================================================
# TABLE
# ======================================================
st.markdown("## 📋 LIVE SENSOR TABLE")

st.dataframe(
    df,
    use_container_width=True,
    height=450
)

# ======================================================
# LIVE CHART
# ======================================================
st.markdown("## 📈 SENSOR ANALYTICS")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Time"],
    y=df["Temperature Reading"],
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
    name='CO'
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0.5)',
    plot_bgcolor='rgba(0,0,0,0.5)',
    font=dict(color='white'),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# AUTO REFRESH
# ======================================================
time.sleep(2)
st.rerun()
