import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)
from scipy.stats import zscore, mode
import numpy as np

# ==============================
# LOAD TRAINED MODEL
# ==============================
model = joblib.load("fire_detection_model.pkl")

# ==============================
# SAMPLE DATASET FOR ANALYTICS
# Replace this with your dataset CSV if available
# ==============================
try:
    dataset = pd.read_csv("fire_dataset.csv")

    X = dataset[['temperature', 'air_quality',
                 'carbon_monoxide', 'smoke']]

    y = dataset['status']

    y_pred = model.predict(X)

except:
    dataset = None

# ==============================
# TITLE
# ==============================
st.title("🔥 IOT BASED FIRE DETECTION AND CLASSIFICATION")

st.write("Enter sensor readings below.")

# ==============================
# INPUTS
# ==============================
temperature = st.number_input("Temperature", format="%.2f")

smoke = int(st.number_input("Smoke", step=1, format="%.0f"))

air_quality = int(
    st.number_input("Air Quality", step=1, format="%.0f")
)

carbon_monoxide = int(
    st.number_input("Carbon Monoxide", step=1, format="%.0f")
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
    # DISPLAY RESULT
    # ==============================
    st.subheader("Prediction Result")

    if prediction == "Fire":
        st.error("🔥 FIRE DETECTED")

    elif prediction == "Potential Fire":
        st.warning("⚠️ POTENTIAL FIRE")

    else:
        st.success("✅ NON-FIRE")

    # ==============================
    # Z-SCORE ANALYSIS
    # ==============================
    st.subheader("📊 Z-Score Analysis")

    z_scores = zscore([
        temperature,
        air_quality,
        carbon_monoxide,
        smoke
    ])

    z_df = pd.DataFrame({
        "Sensor": [
            "Temperature",
            "Air Quality",
            "Carbon Monoxide",
            "Smoke"
        ],
        "Value": [
            temperature,
            air_quality,
            carbon_monoxide,
            smoke
        ],
        "Z-Score": z_scores
    })

    st.dataframe(z_df)

    # ==============================
    # MEAN MEDIAN MODE
    # ==============================
    st.subheader("📈 Statistical Analysis")

    values = [
        temperature,
        air_quality,
        carbon_monoxide,
        smoke
    ]

    mean_value = np.mean(values)
    median_value = np.median(values)
    mode_value = mode(values, keepdims=True).mode[0]

    stats_df = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Mode"],
        "Value": [
            mean_value,
            median_value,
            mode_value
        ]
    })

    st.table(stats_df)

    # ==============================
    # BAR CHART
    # ==============================
    st.subheader("📉 Sensor Readings Chart")

    fig, ax = plt.subplots()

    sensors = [
        "Temperature",
        "Air Quality",
        "CO",
        "Smoke"
    ]

    readings = [
        temperature,
        air_quality,
        carbon_monoxide,
        smoke
    ]

    ax.bar(sensors, readings)

    ax.set_ylabel("Values")
    ax.set_title("Sensor Readings")

    st.pyplot(fig)

# ==============================
# MODEL PERFORMANCE
# ==============================
if dataset is not None:

    st.header("🧠 Model Performance")

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
    # PERFORMANCE TABLE
    # ==============================
    performance_df = pd.DataFrame({
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

    st.subheader("📋 Accuracy Table")
    st.table(performance_df)

    # ==============================
    # CONFUSION MATRIX
    # ==============================
    st.subheader("📌 Confusion Matrix")

    cm = confusion_matrix(y, y_pred)

    cm_df = pd.DataFrame(cm)

    st.dataframe(cm_df)

    # ==============================
    # FALSE POSITIVE / FALSE NEGATIVE
    # ==============================
    if cm.shape == (2, 2):

        tn, fp, fn, tp = cm.ravel()

        error_df = pd.DataFrame({
            "Metric": [
                "True Positive",
                "True Negative",
                "False Positive",
                "False Negative"
            ],
            "Value": [
                tp,
                tn,
                fp,
                fn
            ]
        })

        st.subheader("⚠️ Error Analysis")
        st.table(error_df)

    # ==============================
    # CLASSIFICATION REPORT
    # ==============================
    st.subheader("📝 Classification Report")

    report = classification_report(
        y,
        y_pred,
        output_dict=True
    )

    report_df = pd.DataFrame(report).transpose()

    st.dataframe(report_df)

else:
    st.warning(
        "Dataset file not found. "
        "Add fire_dataset.csv for analytics."
    )
