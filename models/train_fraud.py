import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("processed/transactions.csv")
X = df[["amount", "ip_mismatch", "velocity", "device_mismatch"]]

model = IsolationForest(contamination=0.01)
model.fit(X)

joblib.dump(model, "models/fraud_model.pkl")
