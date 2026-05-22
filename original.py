# =====================================================
# FILE NAME:
# predict_and_control.py
#
# PURPOSE:
# 1. Get RAW sensor data from Supabase
# 2. Run Machine Learning prediction
# 3. Save prediction results to Supabase
# 4. Notify ESP32 to activate:
#       - Relay
#       - Breaker
#       - Buzzer
# 5. Dashboard reads FINAL AI results
#
# ======================================================

# =====================================================
# INSTALL REQUIRED LIBRARIES
# =====================================================
#
# pip install pandas numpy scikit-learn
# pip install supabase joblib
#
# =====================================================

import pandas as pd
import numpy as np
import joblib
from supabase import create_client
from datetime import datetime

# =====================================================
# SUPABASE CONFIGURATION
# =====================================================
# CHANGE THESE
# =====================================================

SUPABASE_URL = "https://cofxcqxbiminjabrptrp.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNvZnhjcXhiaW1pbmphYnJwdHJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1ODEyMDAsImV4cCI6MjA5MjE1NzIwMH0.6FDwnj_AiaOPVoYNiRA43RKDn3cqLYK00rTHuSaNh3c"

# =====================================================
# CONNECT TO SUPABASE
# =====================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================================
# LOAD MACHINE LEARNING MODEL
# =====================================================
# CHANGE THIS IF YOUR FILE NAME IS DIFFERENT
# =====================================================

model = joblib.load("fire_detection_model.pkl")

# =====================================================
# FETCH LATEST RAW SENSOR DATA
# =====================================================
#
# TABLE:
# raw_sensor_readings
#
# =====================================================

response = supabase.table(
    "table1_raw_data"
).select("*").order(
    "Date_and_Time",
    desc=True
).limit(1).execute()

# =====================================================
# CHECK IF EMPTY
# =====================================================

if len(response.data) == 0:

    print("No sensor data found.")

    exit()

# =====================================================
# CONVERT TO DATAFRAME
# =====================================================

df = pd.DataFrame(response.data)

latest = df.iloc[0]

# =====================================================
# GET SENSOR VALUES
# =====================================================

temperature = latest["temperature_reading"]

air_quality = latest["air_quality_reading"]

carbon_monoxide = latest["carbon_monoxide_reading"]

smoke = latest["smoke_reading"]



# =====================================================
# PREPARE ML INPUT
# =====================================================

X = np.array([[
    temperature,
    air_quality,
    carbon_monoxide,
    smoke
   
]])

# =====================================================
# MACHINE LEARNING PREDICTION
# =====================================================

prediction = model.predict(X)[0]

# =====================================================
# PREDICTION PROBABILITY
# =====================================================

try:

    probabilities = model.predict_proba(X)[0]

    fire_probability = float(np.max(probabilities))

except:

    fire_probability = 0.0

# =====================================================
# MACHINE LEARNING CONDITION MAPPING
# =====================================================

condition = str(prediction).upper()

# =====================================================
# NORMAL
# =====================================================

if (
    condition == "NORMAL" or
    condition == "0"
):

    condition = "NORMAL"

    remarks = "System Safe"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# POTENTIAL FIRE
# =====================================================

elif (
    condition == "POTENTIAL FIRE" or
    condition == "POTENTIAL_FIRE" or
    condition == "1"
):

    condition = "POTENTIAL FIRE"

    remarks = "Warning Sent | Buzzer Activated"

    relay_status = False

    breaker_status = False

    buzzer_status = True

# =====================================================
# FIRE
# =====================================================

elif (
    condition == "FIRE" or
    condition == "2"
):

    condition = "FIRE"

    remarks = "Relay Activated | Breaker Tripped | SMS Sent"

    relay_status = True

    breaker_status = True

    buzzer_status = True

# =====================================================
# UNKNOWN
# =====================================================

else:

    condition = "UNKNOWN"

    remarks = "Unknown Prediction"

    relay_status = False

    breaker_status = False

    buzzer_status = False

# =====================================================
# SAVE AI RESULTS TO SUPABASE
# =====================================================
#
# TABLE:
# predicted_sensor_readings
#
# =====================================================

supabase.table(
    "table2_with_MLmodel"
).insert({

    "Date_and_Time":
    datetime.now().isoformat(),

    "temperature_reading":
    float(temperature),

    "air_quality_reading":
    int(air_quality),

    "carbon_monoxide_reading":
    int(carbon_monoxide),
    
    "smoke_reading":
    int(smoke),

    "predicted_condition":
    condition,

    "predicted_remarks":
    remarks,

    "fire_probability":
    fire_probability

}).execute()

# =====================================================
# SEND CONTROL COMMANDS TO ESP32
# =====================================================
#
# TABLE:
# esp32_control
#
# =====================================================

supabase.table(
    "table3_esp_breaker_sms"
).upsert({

    "id": 1,

    "relay_status":
    relay_status,

    "breaker_status":
    breaker_status,

    "buzzer_status":
    buzzer_status,

    "condition":
    condition

}).execute()

# =====================================================
# TERMINAL OUTPUT
# =====================================================

print("=======================================")

print("AI FIRE DETECTION RESULT")

print("=======================================")

print("Temperature:", temperature)

print("Air Quality:", air_quality)

print("Carbon Monoxide:", carbon_monoxide)

print("Smoke:", smoke)

print("Prediction:", prediction)

print("Condition:", condition)

print("Remarks:", remarks)

print("Fire Probability:", fire_probability)

print("Relay:", relay_status)

print("Breaker:", breaker_status)

print("Buzzer:", buzzer_status)

print("=======================================")
