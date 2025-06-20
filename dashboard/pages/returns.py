# dashboard/pages/returns.py
import streamlit as st
import pandas as pd
import joblib
import os

st.title("🔁 Returns Analytics")

# Load data
df = pd.read_csv("processed/returns_train.csv")

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/return_predictor.pkl"))
model = joblib.load(model_path)

# Predict return risk
X = df[["product_age", "return_window", "damaged", "customer_rating"]]
df["return_risk"] = model.predict_proba(X)[:, 1]

# Add a mock product_id for display
df["product_id"] = [f"P{1000+i}" for i in range(len(df))]

# Display top risky products
st.subheader("🚩 Top 10 High Risk Products")
st.write(df[["product_id", "return_risk"]].sort_values("return_risk", ascending=False).head(10))

# Risk by customer rating
st.subheader("📊 Avg Return Risk by Customer Rating")
st.bar_chart(df.groupby("customer_rating")["return_risk"].mean())
