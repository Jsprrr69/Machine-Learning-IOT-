import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import os

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Fire Detection Dashboard",
    page_icon="🔥",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================
st.title("🔥 Fire Detection and Prediction Dashboard")

st.markdown("""
Live monitoring dashboard for:
- MQ2 Smoke Sensor
- MQ135 Air Quality Sensor
- MQ7 Carbon Monoxide Sensor
""")

# ==========================================
# CSV FILE
# ==========================================
CSV_FILE = "sensor_data.csv"

# Create CSV if not existing
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "Time",
        "MQ2",
        "Air",
        "CO"
    ])
    df.to_csv(CSV_FILE, index=False)

# ==========================================
# AUTO REFRESH
# ==========================================
refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)",
    1,
    10,
    2
)

# ==========================================
# LOAD DATA
# ==========================================
df = pd.read_csv(CSV_FILE)

# ==========================================
# CHECK IF DATA EXISTS
# ==========================================
if len(df) == 0:
    st.warning("No sensor data yet.")
    st.stop()

# ==========================================
# LATEST VALUES
# ==========================================
latest = df.iloc[-1]

mq2 = latest["MQ2"]
air = latest["Air"]
co = latest["CO"]

# ==========================================
# FIRE PREDICTION LOGIC
# ==========================================
fire_status = "SAFE"
fire_color = "green"

if mq2 > 2500 or co > 2000 or air > 2500:
    fire_status = "🔥 FIRE DETECTED"
    fire_color = "red"

elif mq2 > 1500 or co > 1200 or air > 1500:
    fire_status = "⚠ WARNING"
    fire_color = "orange"

# ==========================================
# STATUS DISPLAY
# ==========================================
st.markdown(f"""
## Current Condition:
### :{fire_color}[{fire_status}]
""")

# ==========================================
# METRICS
# ==========================================
col1, col2, col3 = st.columns(3)

col1.metric(
    label="MQ2 Smoke",
    value=f"{mq2}"
)

col2.metric(
    label="MQ135 Air Quality",
    value=f"{air}"
)

col3.metric(
    label="MQ7 Carbon Monoxide",
    value=f"{co}"
)

# ==========================================
# LINE CHARTS
# ==========================================
st.subheader("📈 Live Sensor Readings")

fig1 = px.line(
    df,
    x="Time",
    y="MQ2",
    title="MQ2 Smoke Sensor"
)

fig2 = px.line(
    df,
    x="Time",
    y="Air",
    title="MQ135 Air Quality Sensor"
)

fig3 = px.line(
    df,
    x="Time",
    y="CO",
    title="MQ7 Carbon Monoxide Sensor"
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# RAW TABLE
# ==========================================
st.subheader("📋 Sensor Dataset")

st.dataframe(df.tail(20))

# ==========================================
# DOWNLOAD BUTTON
# ==========================================
st.download_button(
    label="⬇ Download Dataset CSV",
    data=df.to_csv(index=False),
    file_name="sensor_dataset.csv",
    mime="text/csv"
)

# ==========================================
# AUTO REFRESH
# ==========================================
time.sleep(refresh_rate)
st.rerun()
