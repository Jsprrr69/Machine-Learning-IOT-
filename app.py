import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
from scipy.stats import zscore, mode
import numpy as np

# ==============================
# LOAD MODEL
# ==============================
model = joblib.load("fire_detection_model.pkl")

# ==============================
# LOAD DATASET
# ==============================
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

# ==============================
# TITLE
# ==============================
st.title("🔥 SeekLiyab Fire Detection System")

st.write("Enter sensor readings below.")

# ==============================
# INPUTS
# ==============================
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

# ==============================
# PREDICT BUTTON
# ==============================
if st.button("Predict"):

    input_data = pd.DataFrame([{
        'temperature': temperature,
        'air_quality': air_quality,
        'carbon_monoxide': carbon_monoxide,
        'smoke': smoke,
    }])

    prediction = model.predict(input_data)[0]

    # ==============================
    # RESULT
    # ==============================
    st.subheader("Prediction Result")

    if prediction == "Fire":
        st.error("🔥 FIRE DETECTED")

    elif prediction == "Potential Fire":
        st.warning("⚠️ POTENTIAL FIRE")

    else:
        st.success("✅ NON-FIRE")

    # ==============================
    # SENSOR BAR GRAPH
    # ==============================
    st.subheader("📊 Sensor Readings")

    sensors = [
        "Temperature",
        "Air Quality",
        "Carbon Monoxide",
        "Smoke"
    ]

    readings = [
        temperature,
        air_quality,
        carbon_monoxide,
        smoke
    ]

    fig1, ax1 = plt.subplots()

    ax1.bar(sensors, readings)

    ax1.set_ylabel("Values")
    ax1.set_title("Sensor Values")

    st.pyplot(fig1)

    # ==============================
    # Z-SCORE BAR GRAPH
    # ==============================
    st.subheader("📈 Z-Score Graph")

    z_scores = zscore(readings)

    fig2, ax2 = plt.subplots()

    ax2.bar(sensors, z_scores)

    ax2.set_ylabel("Z-Score")
    ax2.set_title("Z-Score Analysis")

    st.pyplot(fig2)

    # ==============================
    # MEAN MEDIAN MODE BAR GRAPH
    # ==============================
    st.subheader("📉 Statistical Analysis")

    mean_value = np.mean(readings)
    median_value = np.median(readings)
    mode_value = mode(
        readings,
        keepdims=True
    ).mode[0]

    stats_names = [
        "Mean",
        "Median",
        "Mode"
    ]

    stats_values = [
        mean_value,
        median_value,
        mode_value
    ]

    fig3, ax3 = plt.subplots()

    ax3.bar(stats_names, stats_values)

    ax3.set_ylabel("Value")
    ax3.set_title("Mean / Median / Mode")

    st.pyplot(fig3)

# ==============================
# MODEL ANALYTICS
# ==============================
if dataset is not None:

    st.header("🧠 Model Analytics")

    # ==============================
    # METRICS
    # ==============================
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

    # ==============================
    # ACCURACY BAR GRAPH
    # ==============================
    st.subheader("📊 Accuracy Metrics")

    metric_names = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]

    metric_values = [
        accuracy,
        precision,
        recall,
        f1
    ]

    fig4, ax4 = plt.subplots()

    ax4.bar(metric_names, metric_values)

    ax4.set_ylabel("Score")
    ax4.set_title("Model Performance")

    st.pyplot(fig4)

    # ==============================
    # CONFUSION MATRIX VALUES
    # ==============================
    cm = confusion_matrix(y, y_pred)

    if cm.shape == (2, 2):

        tn, fp, fn, tp = cm.ravel()

        st.subheader("⚠️ Error Analysis")

        error_names = [
            "True Positive",
            "True Negative",
            "False Positive",
            "False Negative"
        ]

        error_values = [
            tp,
            tn,
            fp,
            fn
        ]

        fig5, ax5 = plt.subplots()

        ax5.bar(error_names, error_values)

        ax5.set_ylabel("Count")
        ax5.set_title("Confusion Matrix Analysis")

        st.pyplot(fig5)

else:
    st.warning(
        "Dataset file not found. "
        "Add fire_dataset.csv for analytics."
    )
