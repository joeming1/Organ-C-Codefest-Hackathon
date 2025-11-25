from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from ml.model import SalesModel

router = APIRouter()
model = SalesModel()

class AnomalyInput(BaseModel):
    Weekly_Sales: float
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    Store: int
    Dept: int
    IsHoliday: int

@router.post("/")
def detect_anomaly(data: AnomalyInput):
    df = pd.DataFrame([data.dict()])
    out = model.detect_anomalies(df).iloc[0]

    return {
        "anomaly": int(out["anomaly"]),
        "anomaly_score": float(out["anomaly_score"])
    }
