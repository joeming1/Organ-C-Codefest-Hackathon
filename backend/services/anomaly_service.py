from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df):
    model = IsolationForest(contamination=0.05)
    model.fit(df[["value"]])

    df["anomaly_score"] = model.decision_function(df[["value"]])
    df["is_anomaly"] = model.predict(df[["value"]])  # -1 = anomaly, 1 = normal

    anomalies = df[df["is_anomaly"] == -1]

    return anomalies
