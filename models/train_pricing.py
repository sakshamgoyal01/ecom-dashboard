import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("processed/pricing_data.csv")
X = df[["demand", "competitor_price", "inventory", "ctr"]]
y = df["optimal_price"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/pricing_model.pkl")
