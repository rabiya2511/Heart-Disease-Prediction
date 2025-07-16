import sqlite3
import joblib

# Load trained model
model = joblib.load('heart_model.pkl')

# Connect to SQLite database
conn = sqlite3.connect('heart.db')
cursor = conn.cursor()

# Create table if it doesn't exist
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
        oldpeak REAL,
        slope INTEGER,
        ca INTEGER,
        thal INTEGER,
        prediction INTEGER
    )
''')

# Get input from user
def get_input():
    print("\nEnter Patient Details:")
    age = int(input("Age: "))
    sex = int(input("Sex (1=Male, 0=Female): "))
    cp = int(input("Chest Pain Type (0–3): "))
    trestbps = int(input("Resting Blood Pressure: "))
    chol = int(input("Cholesterol: "))
    fbs = int(input("Fasting Blood Sugar > 120 (1=True, 0=False): "))
    restecg = int(input("Resting ECG (0–2): "))
    thalach = int(input("Maximum Heart Rate Achieved: "))
    exang = int(input("Exercise Induced Angina (1=True, 0=False): "))
    oldpeak = float(input("Oldpeak (ST depression): "))
    slope = int(input("Slope of ST segment (0–2): "))
    ca = int(input("Number of major vessels (0–3): "))
    thal = int(input("Thalassemia (1=Normal, 2=Fixed Defect, 3=Reversible): "))
    
    return [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
            exang, oldpeak, slope, ca, thal]

# Predict
features = get_input()
prediction = model.predict([features])[0]

# Store in database
cursor.execute('''
    INSERT INTO patient_data (
        age, sex, cp, trestbps, chol, fbs, restecg,
        thalach, exang, oldpeak, slope, ca, thal, prediction
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (*features, prediction))

conn.commit()
conn.close()

# Show result
print("\n✅ Prediction:", "💓 At Risk of Heart Disease" if prediction == 1 else "🫀 No Risk")