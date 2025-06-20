# dashboard/pages/customer.py
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

st.title("🛍️ Customer Analytics")
df = pd.read_csv("processed/cleaned_customers.csv")

st.subheader("RFM Segmentation")
fig = px.scatter(df, x="recency", y="frequency", color="monetary", hover_data=["customer_id"])
st.plotly_chart(fig)

st.subheader("Churn Prediction")
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/churn_model.pkl"))
clf = joblib.load(model_path)
X = df[["recency", "frequency", "monetary", "returns"]]
df["churn_prob"] = clf.predict_proba(X)[:, 1]
st.write(df[["customer_id", "churn_prob"]].sort_values("churn_prob", ascending=False).head(10))
