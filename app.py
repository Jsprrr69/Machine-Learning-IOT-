import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
    f1_score
)

from scipy.stats import zscore, mode

# ==========================================
# LOAD MODEL
# ==========================================
model = joblib.load("fire_detection_model.pkl")

# ==========================================
# LOAD DATASET
# ==========================================
try:
    dataset = pd.read_csv("fire_dataset.csv")

    X = dataset[['temperature',
                 'air_quality',
                 'carbon_monoxide',
                 'smoke']]

    y = dataset['label']

    y_pred = model.predict(X)

except:
    dataset = None

# ==========================================
# TITLE
# ==========================================
st.title("🔥 SeekLiyab Fire Detection System")

st.write("Enter sensor readings below.")

# ==========================================
# USER INPUTS
# ==========================================
temperature = st.number_input(
    "Temperature",
    format="%.2f"
)

smoke = int(
    st.number_input(
        "Smoke",
        step=1,
        format="%.0f"
    )
)

air_quality = int(
    st.number_input(
        "Air Quality",
        step=1,
        format="%.0f"
    )
)

carbon_monoxide = int(
    st.number_input(
        "Carbon Monoxide",
        step=1,
        format="%.0f"
    )
)

# ==========================================
# PREDICT BUTTON
# ==========================================
if st.button("Predict"):

    input_data = pd.DataFrame([{
        'temperature': temperature,
        'air_quality': air_quality,
        'carbon_monoxide': carbon_monoxide,
        'smoke': smoke,
    }])

    prediction = model.predict(input_data)[0]

    # ==========================================
    # DISPLAY RESULT
    # ==========================================
    st.subheader("Prediction Result")

    if prediction == "Fire":
        st.error("🔥 FIRE DETECTED")

    elif prediction == "Potential Fire":
        st.warning("⚠️ POTENTIAL FIRE")

    else:
        st.success("✅ NON-FIRE")

    # ==========================================
    # SENSOR GRAPH
    # ==========================================
    st.subheader("📊 Sensor Readings")

    sensors = [
        "Temperature",
        "Air Quality",
        "Carbon Monoxide",
        "Smoke"
    ]

    values = [
        temperature,
        air_quality,
        carbon_monoxide,
        smoke
    ]

    sensor_df = pd.DataFrame({
        "Sensor": sensors,
        "Value": values
    })

    fig_sensor = px.bar(
        sensor_df,
        x="Sensor",
        y="Value",
        title="Sensor Readings"
    )

    st.plotly_chart(fig_sensor, use_container_width=True)

    # ==========================================
    # Z-SCORE GRAPH
    # ==========================================
    st.subheader("📈 Z-Score Analysis")

    z_scores = zscore(values)

    z_df = pd.DataFrame({
        "Sensor": sensors,
        "Z-Score": z_scores
    })

    fig_z = px.bar(
        z_df,
        x="Sensor",
        y="Z-Score",
        title="Z-Score per Sensor"
    )

    st.plotly_chart(fig_z, use_container_width=True)

    # ==========================================
    # MEAN MEDIAN MODE GRAPH
    # ==========================================
    st.subheader("📉 Statistical Analysis")

    mean_value = np.mean(values)
    median_value = np.median(values)
    mode_value = mode(values, keepdims=True).mode[0]

    stats_df = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Mode"],
        "Value": [mean_value, median_value, mode_value]
    })

    fig_stats = px.bar(
        stats_df,
        x="Statistic",
        y="Value",
        title="Mean / Median / Mode"
    )

    st.plotly_chart(fig_stats, use_container_width=True)

# ==========================================
# MODEL ANALYTICS
# ==========================================
if dataset is not None:

    st.header("🧠 Model Analytics")

    # ==========================================
    # OVERALL METRICS
    # ==========================================
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(
        y,
        y_pred,
        average='weighted'
    )

    recall = recall_score(
        y,
        y_pred,
        average='weighted'
    )

    f1 = f1_score(
        y,
        y_pred,
        average='weighted'
    )

    overall_df = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score"
        ],
        "Value": [
            accuracy,
            precision,
            recall,
            f1
        ]
    })

    st.subheader("📊 Overall Performance Metrics")

    fig_metrics = px.bar(
        overall_df,
        x="Metric",
        y="Value",
        title="Overall Model Performance"
    )

    st.plotly_chart(fig_metrics, use_container_width=True)

    # ==========================================
    # CLASS-WISE PERFORMANCE METRICS
    # ==========================================
    st.subheader(
        "📋 Class-Wise Precision, Recall, and F1-Score"
    )

    precision_cls, recall_cls, f1_cls, support = \
        precision_recall_fscore_support(
            y,
            y_pred
        )

    class_labels = np.unique(y)

    class_metrics_df = pd.DataFrame({
        "Class": class_labels,
        "Precision": precision_cls,
        "Recall": recall_cls,
        "F1-Score": f1_cls,
        "Support": support
    })

    st.dataframe(class_metrics_df)

    # ==========================================
    # CLASS-WISE GRAPH
    # ==========================================
    melted_df = class_metrics_df.melt(
        id_vars="Class",
        value_vars=[
            "Precision",
            "Recall",
            "F1-Score"
        ],
        var_name="Metric",
        value_name="Score"
    )

    fig_class = px.bar(
        melted_df,
        x="Class",
        y="Score",
        color="Metric",
        barmode="group",
        title="Class-Wise Performance Metrics"
    )

    st.plotly_chart(fig_class, use_container_width=True)

    # ==========================================
    # CONFUSION MATRIX
    # ==========================================
    st.subheader("📌 Confusion Matrix")

    cm = confusion_matrix(y, y_pred)

    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=class_labels,
            y=class_labels,
            text=cm,
            texttemplate="%{text}",
            colorscale="Blues"
        )
    )

    fig_cm.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Label",
        yaxis_title="True Label"
    )

    st.plotly_chart(fig_cm, use_container_width=True)

else:
    st.warning(
        "Dataset file not found. "
        "Add fire_dataset.csv for analytics."
    )
