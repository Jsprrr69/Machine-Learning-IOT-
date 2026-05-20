import streamlit as st
import pandas as pd
import numpy as np
import joblib

import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_recall_fscore_support,
    accuracy_score
)

from scipy.stats import zscore

# =========================
# LOAD MODEL
# =========================
model = joblib.load("fire_detection_model.pkl")

# =========================
# LOAD DATASET
# =========================
st.title("🔥 SeekLiyab Fire Detection Model Dashboard")

try:
    dataset = pd.read_csv("fire_dataset.csv")

    X = dataset[['temperature', 'air_quality',
                 'carbon_monoxide', 'smoke']]
    y = dataset['label']

    y_pred = model.predict(X)

except Exception as e:
    st.error("Dataset not found or invalid format.")
    st.stop()

# =========================
# BASIC METRICS
# =========================
st.header("📊 Overall Performance")

accuracy = accuracy_score(y, y_pred)

precision, recall, f1, _ = precision_recall_fscore_support(
    y, y_pred, average=None, labels=np.unique(y)
)

class_names = np.unique(y)

df_metrics = pd.DataFrame({
    "Class": class_names,
    "Precision": precision,
    "Recall": recall,
    "F1-Score": f1
})

st.metric("Overall Accuracy", f"{accuracy:.4f}")

st.dataframe(df_metrics)

# =========================
# CONFUSION MATRIX
# =========================
st.subheader("📌 Confusion Matrix")

cm = confusion_matrix(y, y_pred, labels=class_names)

cm_percent = cm / cm.sum(axis=1, keepdims=True)

fig_cm = go.Figure(
    data=go.Heatmap(
        z=cm,
        x=class_names,
        y=class_names,
        colorscale="Blues",
        text=[
            [
                f"{cm[i][j]} ({cm_percent[i][j]*100:.1f}%)"
                for j in range(len(class_names))
            ]
            for i in range(len(class_names))
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
# CLASS-WISE GRAPHS
# =========================
st.subheader("📊 Class-wise Performance")

fig_p = px.bar(df_metrics, x="Class", y="Precision", title="Precision by Class", text_auto=True)
fig_r = px.bar(df_metrics, x="Class", y="Recall", title="Recall by Class", text_auto=True)
fig_f = px.bar(df_metrics, x="Class", y="F1-Score", title="F1-Score by Class", text_auto=True)

st.plotly_chart(fig_p, use_container_width=True)
st.plotly_chart(fig_r, use_container_width=True)
st.plotly_chart(fig_f, use_container_width=True)

# =========================
# Z-SCORE ANALYSIS (MODEL BEHAVIOR)
# =========================
st.subheader("📉 Z-Score Analysis (Prediction Distribution)")

# Encode predictions into numeric values
label_map = {label: idx for idx, label in enumerate(class_names)}
y_encoded = np.array([label_map[i] for i in y])
y_pred_encoded = np.array([label_map[i] for i in y_pred])

errors = y_pred_encoded - y_encoded

z_scores = zscore(errors)

df_z = pd.DataFrame({
    "Sample": np.arange(len(z_scores)),
    "Z-Score": z_scores
})

fig_z = px.line(df_z, x="Sample", y="Z-Score",
                title="Prediction Error Z-Score Distribution")

st.plotly_chart(fig_z, use_container_width=True)

st.write("### Interpretation")
st.write("- Values near 0 → normal predictions")
st.write("- High positive/negative spikes → misclassified samples")
