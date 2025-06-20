# dashboard/pages/8_fraud.py
import streamlit as st
import pandas as pd
import joblib
import os

st.title("🔐 Transaction Fraud Detection")
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/fraud_model.pkl"))
model = joblib.load(model_path)
df = pd.read_csv("processed/transactions.csv")
X = df[["amount", "ip_mismatch", "velocity", "device_mismatch"]]

df["fraud_score"] = model.decision_function(X)
df["is_fraud"] = model.predict(X)

st.write("Potential Fraudulent Transactions:")
st.dataframe(df[df["is_fraud"] == -1].head(10))
