import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("processed/cleaned_customers.csv")
X = df[["recency", "frequency", "monetary", "returns"]]
y = df["churn"]  # 0 or 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

joblib.dump(clf, "models/churn_model.pkl")