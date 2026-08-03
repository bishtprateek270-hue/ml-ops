import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load processed train data
train = pd.read_csv("data/train.csv")

# Extract features and label
X_train = train[["Age", "Salary"]]
y_train = train["Purchased"]

# Train model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
print("Model saved to models/model.pkl")
