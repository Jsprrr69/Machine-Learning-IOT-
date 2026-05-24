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
DATA_PATH = "testingset.csv"

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

# convert to %
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
            [f"{cm[i][j]} ({cm_percent[i][j]:.1f}%)" for j in range(len(classes))]
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

sensor_features = ['temperature', 'air_quality', 'carbon_monoxide', 'smoke']

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

fig_corr.update_layout(title="Sensor Correlation Matrix")

st.plotly_chart(fig_corr, use_container_width=True)
