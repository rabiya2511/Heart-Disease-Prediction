import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your CSV
file_path = r"C:\heart disease project\heart disease\heart_disease_uci.csv"
data = pd.read_csv(file_path)

# Drop unneeded columns
data = data.drop(['id', 'dataset'], axis=1)

# Convert 'num' to binary target: 0 = no disease, >0 = disease
data['target'] = data['num'].apply(lambda x: 1 if x > 0 else 0)
data.drop('num', axis=1, inplace=True)

# Encode categorical columns
categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
le = LabelEncoder()
for col in categorical_cols:
    data[col] = le.fit_transform(data[col].astype(str))

# Drop rows with missing values (NaN)
data = data.dropna()

# Split features and labels
X = data.drop('target', axis=1)
y = data['target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'heart_model.pkl')
print("✅ Model trained and saved as heart_model.pkl")