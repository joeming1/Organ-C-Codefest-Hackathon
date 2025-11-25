from fastapi import APIRouter
import pandas as pd
from ml.model import SalesModel
from pydantic import BaseModel

router = APIRouter()
model = SalesModel()

class RiskInput(BaseModel):
    Weekly_Sales: float
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    Store: int
    Dept: int
    IsHoliday: int

@router.post("/")
def risk(data: RiskInput):

    df = pd.DataFrame([data.dict()])

    # anomaly
    anomaly_out = model.detect_anomalies(df).iloc[0]
    anomaly_flag = int(anomaly_out["anomaly"])
    anomaly_score = float(anomaly_out["anomaly_score"])

    # cluster
    cluster_id = model.cluster(df)

    # build risk score
    score = 0
    if anomaly_flag == -1:
        score += 40
    if abs(anomaly_score) > 0.15:
        score += 10
    if cluster_id in [6, 7]:
        score += 20

    # risk level
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": score,
        "risk_level": level,
        "cluster": cluster_id,
        "anomaly": anomaly_flag,
        "anomaly_score": anomaly_score
    }
