from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from ml.model import SalesModel

router = APIRouter()
model = SalesModel()

class ClusterInput(BaseModel):
    Weekly_Sales: float
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    Store: int
    Dept: int
    IsHoliday: int

@router.post("/")
def cluster(data: ClusterInput):
    df = pd.DataFrame([data.dict()])
    cluster_id = model.cluster(df)
    return {"cluster": cluster_id}
