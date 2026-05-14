import streamlit as st
import pandas as pd
import joblib

# LOAD TRAINED MODEL
model = joblib.load("fire_detection_model.pkl")

# TITLE
st.title("🔥 SeekLiyab Fire Detection System")

st.write("Enter sensor readings below.")

# INPUTS
temperature = st.number_input("Temperature")
smoke = st.number_input("Smoke")
air_quality = st.number_input("Air Quality")
carbon_monoxide = st.number_input("Carbon Monoxide")

# PREDICT BUTTON
if st.button("Predict"):

    input_data = pd.DataFrame([{
        'temperature': temperature,
        'smoke': smoke,
        'air_quality': air_quality,
        'carbon_monoxide': carbon_monoxide
    }])

    prediction = model.predict(input_data)[0]

    # DISPLAY RESULT
    if prediction == "Fire":
        st.error("🔥 FIRE DETECTED")

    elif prediction == "Potential Fire":
        st.warning("⚠️ POTENTIAL FIRE")

    else:
        st.success("✅ NON-FIRE")
