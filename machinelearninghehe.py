# ================================
# SEEKLIYAB FIRE DETECTION TRAINING
# Random Forest Classifier
# ================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# LOAD DATASET
# ==========================================

# Replace with your dataset filename
df = pd.read_csv("testingset3.csv")

# ==========================================
# DATASET FORMAT
# ==========================================
# Your CSV should contain:
#
# temperature
# smoke
# air_quality
# carbon_monoxide
# status
#
# Example:
#
# temperature,smoke,air_quality,carbon_monoxide,status
# 30,120,150,10,Non-Fire
# 45,600,500,120,Potential Fire
# 70,1500,900,500,Fire
#
# ==========================================

# FEATURES
X = df[[
    'temperature',
    'air_quality',
    'carbon_monoxide',
    'smoke',
    
 
]]

# TARGET
y = df['status']

# ==========================================
# TRAIN TEST SPLIT
# 70% TRAIN
# 30% TEST
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# ==========================================
# RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

# TRAIN MODEL
model.fit(X_train, y_train)

# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL ACCURACY")
print("==============================")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")
print(classification_report(y_test, y_pred))

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")
print(confusion_matrix(y_test, y_pred))

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, "fire_detection_model.pkl")

print("\nModel saved as fire_detection_model.pkl")
