import mlflow.pyfunc
import pandas as pd

# Load the MLflow model
model = mlflow.pyfunc.load_model(
    "mlruns/1/models/m-2a4c27becbe64ac2b4e509ac2a34c155/artifacts"
)

# Sample house data
home = pd.DataFrame([
    {
        "LotArea": 9000,
        "OverallQual": 7,
        "OverallCond": 5,
        "YearBuilt": 2010,
        "GrLivArea": 1900,
        "GarageCars": 2
    }
])

# Predict
prediction = model.predict(home)

print("Predicted House Price:", prediction[0])
