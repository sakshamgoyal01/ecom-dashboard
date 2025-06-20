# dashboard/streamlit_app.py
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="E-Commerce Intelligence", layout="wide")

st.sidebar.title("🧠 E-Com Intelligence Hub")
st.sidebar.markdown("Select an analytics module:")

st.sidebar.success("Use the menu to navigate the dashboards.")

st.title("📊 Unified E-Commerce Analytics Dashboard")
st.markdown(
    """
    Welcome to the AI-powered dashboard simulating analytics for companies like Amazon, Flipkart, Walmart, and Myntra.

    Use the side panel to explore:
    - Customer churn
    - Product recommendations
    - Returns and delivery analysis
    - Real-time fraud detection
    """
)
