import streamlit as st
import pandas as pd
import joblib
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import (
    confusion_matrix,
    precision_recall_fscore_support,
    accuracy_score
)

from scipy.stats import zscore, mode

# =========================
# LOAD MODEL
# =========================
model = joblib.load("fire_detection_model.pkl")

# =========================
# LOAD DATASET (FOR ANALYTICS)
# =========================
try:
    dataset = pd.read_csv("fire_dataset.csv")

    X = dataset[['temperature', 'air_quality',
                 'carbon_monoxide', 'smoke']]

    y = dataset['label']

    y_pred = model.predict(X)

except:
    dataset = None

# =========================
# UI TITLE
# =========================
st.title("🔥 SeekLiyab Fire Detection System")
st.write("Enter sensor readings below")

# =========================
# INPUTS
# =========================
temperature = st.number_input("Temperature", format="%.2f")
smoke = int(st.number_input("Smoke", step=1, format="%.0f"))
air_quality = int(st.number_input("Air Quality", step=1, format="%.0f"))
carbon_monoxide = int(st.number_input("Carbon Monoxide", step=1, format="%.0f"))

# =========================
# PREDICTION
# =========================
if st.button("Predict"):

    input_data = pd.DataFrame([{
        "temperature": temperature,
        "air_quality": air_quality,
        "carbon_monoxide": carbon_monoxide,
        "smoke": smoke
    }])

    prediction = model.predict(input_data)[0]

    st.subheader("Prediction Result")

    if prediction == "Fire":
        st.error("🔥 FIRE DETECTED")
    elif prediction == "Potential Fire":
        st.warning("⚠️ POTENTIAL FIRE")
    else:
        st.success("✅ NON-FIRE")

    # =========================
    # SENSOR BAR GRAPH
    # =========================
    sensors = ["Temperature", "Air Quality", "CO", "Smoke"]
    values = [temperature, air_quality, carbon_monoxide, smoke]

    df_sensor = pd.DataFrame({
        "Sensor": sensors,
        "Value": values
    })

    fig = px.bar(df_sensor, x="Sensor", y="Value", title="Sensor Readings")
    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Z-SCORE GRAPH
    # =========================
    z_vals = zscore(values)

    df_z = pd.DataFrame({
        "Sensor": sensors,
        "Z-Score": z_vals
    })

    figz = px.bar(df_z, x="Sensor", y="Z-Score", title="Z-Score Analysis")
    st.plotly_chart(figz, use_container_width=True)

    # =========================
    # MEAN / MEDIAN / MODE
    # =========================
    mean_v = np.mean(values)
    median_v = np.median(values)
    mode_v = mode(values, keepdims=True).mode[0]

    df_stats = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Mode"],
        "Value": [mean_v, median_v, mode_v]
    })

    fig_stats = px.bar(df_stats, x="Statistic", y="Value",
                       title="Mean / Median / Mode")
    st.plotly_chart(fig_stats, use_container_width=True)

# =========================
# MODEL ANALYTICS SECTION
# =========================
if dataset is not None:

    st.header("🧠 Model Performance Analytics")

    # =========================
    # CONFUSION MATRIX
    # =========================
    st.subheader("📌 Confusion Matrix")

    cm = confusion_matrix(y, y_pred)
    labels = np.unique(y)

    cm_percent = cm / cm.sum(axis=1, keepdims=True) * 100

    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale="Blues",
            text=[
                [
                    f"{cm[i][j]} ({cm_percent[i][j]:.1f}%)"
                    for j in range(len(labels))
                ]
                for i in range(len(labels))
            ],
            texttemplate="%{text}"
        )
    )

    fig_cm.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Class",
        yaxis_title="Actual Class"
    )

    st.plotly_chart(fig_cm, use_container_width=True)

    # =========================
    # CLASS-WISE METRICS
    # =========================
    st.subheader("📊 Class-wise Metrics")

    precision, recall, f1, _ = precision_recall_fscore_support(
        y, y_pred
    )

    class_names = np.unique(y)

    df_metrics = pd.DataFrame({
        "Class": class_names,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1
    })

    st.dataframe(df_metrics)

    # =========================
    # PRECISION
    # =========================
    fig_p = px.bar(df_metrics, x="Class", y="Precision",
                   text_auto=".3f", title="Precision")
    st.plotly_chart(fig_p, use_container_width=True)

    # =========================
    # RECALL
    # =========================
    fig_r = px.bar(df_metrics, x="Class", y="Recall",
                   text_auto=".3f", title="Recall")
    st.plotly_chart(fig_r, use_container_width=True)

    # =========================
    # F1 SCORE
    # =========================
    fig_f = px.bar(df_metrics, x="Class", y="F1-Score",
                   text_auto=".3f", title="F1-Score")
    st.plotly_chart(fig_f, use_container_width=True)

    # =========================
    # ACCURACY
    # =========================
    acc = accuracy_score(y, y_pred)

    st.metric("Overall Accuracy", f"{acc:.4f}")

else:
    st.warning("Upload dataset (fire_dataset.csv) for analytics.")
