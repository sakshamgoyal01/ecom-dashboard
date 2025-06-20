# dashboard/pages/6_sentiment.py
import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

st.title("💬 Sentiment Analysis on Reviews")

# Load review data
df = pd.read_csv("processed/reviews.csv")

# Sentiment analysis
df["sentiment"] = df["review_text"].apply(lambda x: TextBlob(x).sentiment.polarity)

# Show results
st.subheader("🔍 Sample Sentiment Scores")
st.write(df[["product_id", "review_text", "sentiment"]].head(10))

# Plot histogram
st.subheader("📊 Sentiment Distribution")
fig, ax = plt.subplots()
df["sentiment"].hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
ax.set_title("Sentiment Polarity Distribution")
ax.set_xlabel("Polarity Score")
ax.set_ylabel("Frequency")

st.pyplot(fig)
