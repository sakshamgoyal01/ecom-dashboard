import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("processed/returns_train.csv")
X = df[["product_age", "return_window", "damaged", "customer_rating"]]
y = df["return"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "models/return_predictor.pkl")