import streamlit as st
import numpy as np
import joblib
import sqlite3

# Load model
model = joblib.load('heart_model.pkl')

# Connect to SQLite database
conn = sqlite3.connect('heart.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        sex INTEGER,
        cp INTEGER,
        trestbps INTEGER,
        chol INTEGER,
        fbs INTEGER,
        restecg INTEGER,
        thalach INTEGER,
        exang INTEGER,
        prediction INTEGER
    )
''')

st.title("❤ Heart Disease Prediction App")
st.write("Enter patient details below to predict risk of heart disease")

# Input fields
age = st.number_input("Age", min_value=10, max_value=120)
sex = st.selectbox("Sex", ["Female", "Male"])
cp = st.selectbox("Chest Pain Type (0–3)", [0, 1, 2, 3])
trestbps = st.number_input("Resting Blood Pressure", min_value=80, max_value=200)
chol = st.number_input("Cholesterol", min_value=100, max_value=600)
fbs = st.selectbox("Fasting Blood Sugar > 120", [0, 1])
restecg = st.selectbox("Resting ECG (0–2)", [0, 1, 2])
thalach = st.number_input("Max Heart Rate", min_value=60, max_value=220)
exang = st.selectbox("Exercise Induced Angina", [0, 1])

if st.button("Predict"):
    sex_val = 1 if sex == "Male" else 0
    features = np.array([[age, sex_val, cp, trestbps, chol, fbs, restecg, thalach, exang]])
    prediction = model.predict(features)[0]

    cursor.execute('''
        INSERT INTO patient_data (
            age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (*features[0], prediction))
    conn.commit()

    if prediction == 1:
        st.error("⚠ High Risk of Heart Disease")
    else:
        st.success("✅ No Risk of Heart Disease")

conn.close()