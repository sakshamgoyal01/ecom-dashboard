# dashboard/pages/5_pricing.py
import streamlit as st
import pandas as pd
import joblib
import os

st.title("💰 Dynamic Pricing Engine")
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/pricing_model.pkl"))
model = joblib.load(model_path)

st.subheader("Price Suggestion")
demand = st.slider("Demand Score", 0, 100)
competitor = st.slider("Competitor Price", 100, 500)
inventory = st.slider("Inventory Level", 0, 1000)
ctr = st.slider("CTR %", 0.0, 1.0)

if st.button("Suggest Price"):
    pred = model.predict([[demand, competitor, inventory, ctr]])
    st.success(f"Optimal Price: ₹{round(pred[0], 2)}")
