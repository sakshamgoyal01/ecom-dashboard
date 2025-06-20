# dashboard/pages/7_sellers.py
import streamlit as st
import pandas as pd

st.title("🧾 Seller Performance")

df = pd.read_csv("processed/seller_scores.csv")

st.subheader("Top Sellers by Dispatch Rate")
st.dataframe(df.sort_values("dispatch_rate", ascending=False).head(10))

st.subheader("High Return Sellers")
st.bar_chart(df.groupby("seller_id")["return_rate"].mean().nlargest(10))
