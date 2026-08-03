import pandas as pd
import joblib
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load test data and model
test = pd.read_csv("data/test.csv")
model = joblib.load("models/model.pkl")

# Extract features and label
X_test = test[["Age", "Salary"]]
y_test = test["Purchased"]

# Generate predictions
print("Evaluating model...")
preds = model.predict(X_test)

# Calculate metrics
metrics = {
    "accuracy": accuracy_score(y_test, preds),
    "precision": precision_score(y_test, preds),
    "recall": recall_score(y_test, preds),
    "f1": f1_score(y_test, preds)
}

# Save metrics to json file
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Evaluation completed. Metrics saved to metrics.json:")
print(json.dumps(metrics, indent=4))
