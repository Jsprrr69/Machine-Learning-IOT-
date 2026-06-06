import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import (
    confusion_matrix,
    precision_recall_fscore_support,
    accuracy_score
)

from scipy.stats import zscore

# =========================
# LOAD MODEL
# =========================
model = joblib.load("fire_detection_model.pkl")

# =========================
# TITLE
# =========================
st.title("🔥 IOT BASED FIRE DETECTION AND CLASSIFICATION")

# =========================
# DATASET HANDLING
# =========================
DATA_PATH = "testingset3.csv"

dataset = None

if os.path.exists(DATA_PATH):
    dataset = pd.read_csv(DATA_PATH)
    st.success("Dataset loaded successfully!")
else:
    st.warning("fire_dataset.csv not found. Upload your dataset.")
    uploaded_file = st.file_uploader("Upload fire_dataset.csv", type=["csv"])

    if uploaded_file is not None:
        dataset = pd.read_csv(uploaded_file)
        st.success("Dataset uploaded successfully!")

if dataset is None:
    st.stop()

# =========================
# CLEAN COLUMNS
# =========================
dataset.columns = dataset.columns.str.strip()

# =========================
# STATISTICAL ANALYSIS TABLES
# =========================
st.subheader("📋 Table 2. Statistical Analysis by Fire Classification")

# =========================
# TEMPERATURE STATISTICS
# =========================
st.markdown("### 🌡️ Temperature Statistics")

temp_stats = (
    dataset.groupby('status')['temperature']
    .agg(['mean', 'std', 'min', 'max'])
    .round(2)
)

st.dataframe(temp_stats, use_container_width=True)

# =========================
# AIR QUALITY STATISTICS
# =========================
st.markdown("### 🌫️ Air Quality Statistics")

aq_stats = (
    dataset.groupby('status')['air_quality']
    .agg(['mean', 'std', 'min', 'max'])
    .round(2)
)

st.dataframe(aq_stats, use_container_width=True)

# =========================
# CARBON MONOXIDE STATISTICS
# =========================
st.markdown("### ☠️ Carbon Monoxide Statistics")

co_stats = (
    dataset.groupby('status')['carbon_monoxide']
    .agg(['mean', 'std', 'min', 'max'])
    .round(2)
)

st.dataframe(co_stats, use_container_width=True)

# =========================
# SMOKE STATISTICS
# =========================
st.markdown("### 🔥 Smoke Statistics")

smoke_stats = (
    dataset.groupby('status')['smoke']
    .agg(['mean', 'std', 'min', 'max'])
    .round(2)
)

st.dataframe(smoke_stats, use_container_width=True)    

# =========================
# TABLE 1. TRAINING DATA STATISTICS
# =========================
st.subheader("📋 Table 1. Training Data Statistics")

stats_table = dataset.groupby('status').agg({
    'temperature': ['mean', 'median', 'min', 'max'],
    'air_quality': ['mean', 'median', 'min', 'max'],
    'carbon_monoxide': ['mean', 'median', 'min', 'max'],
    'smoke': ['mean', 'median', 'min', 'max']
}).round(3)

# Convert MultiIndex column names
stats_table.columns = [
    f"{col[0]}_{col[1]}"
    for col in stats_table.columns
]

stats_table = stats_table.reset_index()

st.dataframe(
    stats_table,
    use_container_width=True
)

# =========================
# FEATURES / LABEL
# =========================
X = dataset[['temperature', 'air_quality', 'carbon_monoxide', 'smoke']]

label_col = "status"
y = dataset[label_col]

y_pred = model.predict(X)

classes = np.unique(y)

# =========================
# ACCURACY
# =========================
accuracy = accuracy_score(y, y_pred) * 100

st.subheader("🎯 Model Accuracy")

df_acc = pd.DataFrame({
    "Metric": ["Accuracy"],
    "Value": [accuracy]
})

fig_acc = px.bar(
    df_acc,
    x="Metric",
    y="Value",
    text_auto=".2f",
    title="Accuracy (%)",
    color_discrete_sequence=["red"]
)

fig_acc.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig_acc, use_container_width=True)

# =========================
# CLASS METRICS
# =========================
precision, recall, f1, _ = precision_recall_fscore_support(
    y, y_pred, average=None, labels=classes
)

precision *= 100
recall *= 100
f1 *= 100

df_metrics = pd.DataFrame({
    "Class": classes,
    "Precision (%)": precision,
    "Recall (%)": recall,
    "F1-Score (%)": f1
})

st.subheader("📊 Class-wise Metrics")

fig_metrics = px.bar(
    df_metrics,
    x="Class",
    y=["Precision (%)", "Recall (%)", "F1-Score (%)"],
    barmode="group",
    title="Class-wise Performance (%)",
    color_discrete_sequence=["red", "darkred", "firebrick"]
)

st.plotly_chart(fig_metrics, use_container_width=True)

# =========================
# F1 SCORE ONLY
# =========================
st.subheader("📊 F1-Score per Class")

df_f1 = pd.DataFrame({
    "Class": classes,
    "F1-Score (%)": f1
})

fig_f1 = px.bar(
    df_f1,
    x="Class",
    y="F1-Score (%)",
    text_auto=".2f",
    title="F1-Score per Class (%)",
    color_discrete_sequence=["darkred"]
)

st.plotly_chart(fig_f1, use_container_width=True)

# =========================
# CONFUSION MATRIX
# =========================
st.subheader("📌 Confusion Matrix")

cm = confusion_matrix(y, y_pred, labels=classes)

cm_percent = cm / cm.sum(axis=1, keepdims=True) * 100

fig_cm = go.Figure(
    data=go.Heatmap(
        z=cm,
        x=classes,
        y=classes,
        colorscale="Reds",
        text=[
            [f"{cm[i][j]} ({cm_percent[i][j]:.1f}%)"
             for j in range(len(classes))]
            for i in range(len(classes))
        ],
        texttemplate="%{text}"
    )
)

fig_cm.update_layout(
    title="Confusion Matrix",
    xaxis_title="Predicted",
    yaxis_title="Actual"
)

st.plotly_chart(fig_cm, use_container_width=True)

# =========================
# Z-SCORE ANALYSIS
# =========================
st.subheader("📉 Z-Score Analysis")

label_map = {label: i for i, label in enumerate(classes)}

y_encoded = np.array([label_map[i] for i in y])
y_pred_encoded = np.array([label_map[i] for i in y_pred])

errors = y_pred_encoded - y_encoded
z_scores = zscore(errors)

df_z = pd.DataFrame({
    "Index": np.arange(len(z_scores)),
    "Z-Score": z_scores
})

fig_z = px.line(
    df_z,
    x="Index",
    y="Z-Score",
    title="Prediction Error Z-Score",
    color_discrete_sequence=["red"]
)

st.plotly_chart(fig_z, use_container_width=True)

# =========================
# SENSOR CORRELATION MATRIX
# =========================
st.subheader("🔥 Sensor Correlation Matrix")

sensor_features = [
    'temperature',
    'air_quality',
    'carbon_monoxide',
    'smoke'
]

corr = dataset[sensor_features].corr()

fig_corr = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=sensor_features,
        y=sensor_features,
        colorscale="Reds",
        zmin=-1,
        zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}"
    )
)

fig_corr.update_layout(
    title="Sensor Correlation Matrix"
)

st.plotly_chart(fig_corr, use_container_width=True)


accuracy = accuracy_score(y, y_pred) * 100
error = 100 - accuracy

st.subheader("🎯 Model Accuracy (Circular View)")

fig_acc = go.Figure()

# Accuracy + Error as donut (circular bar style)
fig_acc.add_trace(go.Pie(
    values=[accuracy, error],
    labels=["Accuracy", "Error"],
    hole=0.75,   # 👈 makes it circular (donut style)
    marker_colors=["red", "black"],
    textinfo="label+percent",
    rotation=90
))

# Center text (big accuracy value)
fig_acc.update_layout(
    annotations=[
        dict(
            text=f"{accuracy:.2f}%",
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False
        )
    ],
    showlegend=True
)

st.plotly_chart(fig_acc, use_container_width=True)
