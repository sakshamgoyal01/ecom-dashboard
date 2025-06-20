import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📦 Delivery Performance Dashboard")

df = pd.read_csv("processed/delivery_data.csv")

# Ensure datetime conversion
df["actual_delivery"] = pd.to_datetime(df["actual_delivery"])
df["expected_delivery"] = pd.to_datetime(df["expected_delivery"])

# Calculate delay (in days)
df["delay"] = (df["actual_delivery"] - df["expected_delivery"]).dt.days

# Show top 10 delayed orders
st.subheader("🚨 Top 10 Most Delayed Deliveries")
st.write(df.sort_values("delay", ascending=False)[["order_id", "actual_delivery", "expected_delivery", "delay"]].head(10))

# Plot average delay by shipping method (if available)
if "shipping_method" in df.columns:
    st.subheader("📊 Avg Delay by Shipping Method")
    delay_chart = df.groupby("shipping_method")["delay"].mean()
    st.bar_chart(delay_chart)