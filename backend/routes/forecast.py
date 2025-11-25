from fastapi import APIRouter, Query
from data_loader import get_time_series
from ml.model import SalesModel

router = APIRouter()
model = SalesModel()

@router.get("/")
def get_forecast(
    store_id: int | None = Query(default=None),
    periods: int = Query(default=6, ge=1, le=26)
):
    # Load real time-series data from CSV
    ts_df = get_time_series(store_id)

    # Call your trained forecast model
    forecast_df = model.forecast(ts_df, periods=periods)

    # Format output
    forecast_df["timestamp"] = forecast_df["timestamp"].dt.strftime("%Y-%m-%d")

    return forecast_df.to_dict(orient="records")
