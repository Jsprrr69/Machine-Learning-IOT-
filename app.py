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
st.title("🔥 SeekLiyab Fire Detection Model Dashboard")

# =========================
# DATASET HANDLING (FIXED)
# =========================
DATA_PATH = "fire_dataset.csv"

dataset = None

if os.path.exists(DATA_PATH):
    dataset = pd.read_csv(DATA_PATH)
    st.success("Dataset loaded successfully!")
else:
    st.warning("fire_dataset.csv not found. Please upload your dataset.")

    uploaded_file = st.file_uploader("Upload fire_dataset.csv", type=["csv"])

    if uploaded_file is not None:
        dataset = pd.read_csv(uploaded_file)
        st.success("Dataset uploaded successfully!")

# STOP if no dataset
if dataset is None:
    st.stop()

# =========================
# FEATURES / LABEL
# =========================
X = dataset[['temperature', 'air_quality', 'carbon_monoxide', 'smoke']]
y = dataset['status']

y_pred = model.predict(X)

# =========================
# METRICS
# =========================
st.header("📊 Model Performance")

accuracy = accuracy_score(y, y_pred)

precision, recall, f1, _ = precision_recall_fscore_support(
    y, y_pred, average=None, labels=np.unique(y)
)

classes = np.unique(y)

df_metrics = pd.DataFrame({
    "Class": classes,
    "Precision": precision,
    "Recall": recall,
    "F1-Score": f1
})

st.metric("Overall Accuracy", f"{accuracy:.4f}")
st.dataframe(df_metrics)

# =========================
# =========================
# CONFUSION MATRIX (RED)
# =========================
st.subheader("📌 Confusion Matrix")

cm = confusion_matrix(y, y_pred, labels=classes)

fig = go.Figure(
    data=go.Heatmap(
        z=cm,
        x=classes,
        y=classes,
        colorscale="Reds",   # 🔥 CHANGED HERE
        text=cm,
        texttemplate="%{text}"
    )
)

fig.update_layout(
    title="Confusion Matrix",
    xaxis_title="Predicted",
    yaxis_title="Actual"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# Z-SCORE ANALYSIS (RED LINE)
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
    color_discrete_sequence=["red"]  # 🔥 CHANGED HERE
)

st.plotly_chart(fig_z, use_container_width=True)

# =========================
# METRICS TABLE (OPTIONAL RED STYLE)
# =========================
fig_metrics = px.bar(
    df_metrics,
    x="Class",
    y=["Precision", "Recall", "F1-Score"],
    barmode="group",
    title="Class-wise Metrics",
    color_discrete_sequence=["red", "darkred", "firebrick"]
)

st.plotly_chart(fig_metrics, use_container_width=True)
fig_z = px.line(df_z, x="Index", y="Z-Score", title="Prediction Error Z-Score")

st.plotly_chart(fig_z, use_container_width=True)
