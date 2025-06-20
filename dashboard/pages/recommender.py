import pandas as pd
import numpy as np
import joblib
import streamlit as st

# Load model + user-item matrix
svd, user_item_matrix = joblib.load("models/recommender_model.pkl")

# List of users
users = user_item_matrix.index.tolist()

st.title("🧠 Product Recommender (SVD)")

# Select a user
user_id = st.selectbox("Select User ID", users)

# Get reconstructed matrix (predicted ratings)
user_vector = svd.transform(user_item_matrix.loc[[user_id]])  # shape: (1, k)
reconstructed_ratings = np.dot(user_vector, svd.components_)  # shape: (1, n_items)

# Convert to pandas Series
predicted_ratings = pd.Series(reconstructed_ratings.flatten(), index=user_item_matrix.columns)

# Filter out already interacted items
seen_items = user_item_matrix.loc[user_id]
unseen = predicted_ratings[seen_items == 0]

# Top-N recommendations
top_n = st.slider("How many recommendations?", 5, 20, 10)
top_recommendations = unseen.sort_values(ascending=False).head(top_n)

# Show results
st.subheader(f"🎯 Top {top_n} Product Recommendations for {user_id}")
st.write(top_recommendations.reset_index().rename(columns={0: "Predicted Rating"}))
