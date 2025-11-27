from fastapi import APIRouter, Query
from typing import Optional, List
import pandas as pd
from ml.model import get_model
from data_loader import load_raw_data
from routes.schemas import SalesDataInput, AnomalyResponse

router = APIRouter()

@router.get("/")
def get_anomalies(
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    dept: Optional[int] = Query(None, description="Filter by department")
):
    """
    Get historical anomaly detection results.
    Returns anomalies from the dataset based on filters.
    """
    model = get_model()
    df = load_raw_data()
    
    # Apply filters
    if store_id is not None:
        df = df[df['Store'] == store_id]
    if dept is not None:
        df = df[df['Dept'] == dept]
    
    # Limit to recent data for performance
    df = df.tail(1000)
    
    # Detect anomalies on filtered data
    result_df = model.detect_anomalies(df)
    
    # Return top anomalies (anomaly == -1)
    anomalies = result_df[result_df['anomaly'] == -1].head(100)
    
    results = []
    for _, row in anomalies.iterrows():
        results.append({
            "date": str(row.get('Date', '')),
            "store": int(row['Store']),
            "dept": int(row['Dept']) if 'Dept' in row else None,
            "weekly_sales": float(row['Weekly_Sales']),
            "anomaly": int(row['anomaly']),
            "anomaly_score": float(row['anomaly_score'])
        })
    
    return results

@router.post("/", response_model=AnomalyResponse)
def detect_anomaly(data: SalesDataInput):
    """
    Detect if a single data point is an anomaly.
    """
    df = pd.DataFrame([data.dict()])
    model = get_model()  # Get singleton instance
    out = model.detect_anomalies(df).iloc[0]

    return {
        "anomaly": int(out["anomaly"]),
        "anomaly_score": float(out["anomaly_score"])
    }
