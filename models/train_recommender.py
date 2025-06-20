import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import joblib

# Load dataset
df = pd.read_csv("processed/user_item.csv")
df['rating'] = df.get('rating', 1.0)

# Create User-Item matrix
user_item_matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

# Matrix factorization using SVD
svd = TruncatedSVD(n_components=20, random_state=42)
latent_matrix = svd.fit_transform(user_item_matrix)

# Save model and matrix
joblib.dump((svd, user_item_matrix), "models/recommender_model.pkl")
print("✅ Pure-Python recommender model saved!")