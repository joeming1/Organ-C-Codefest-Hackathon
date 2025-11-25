from fastapi import APIRouter
from data_loader import load_raw_data

router = APIRouter()

@router.get("/")
def kpi_overview(store_id: int = None, dept: int = None):
    df = load_raw_data()

    if store_id:
        df = df[df["Store"] == store_id]
    if dept:
        df = df[df["Dept"] == dept]

    return {
        "avg_weekly_sales": float(df["Weekly_Sales"].mean()),
        "max_sales": float(df["Weekly_Sales"].max()),
        "min_sales": float(df["Weekly_Sales"].min()),
        "volatility": float(df["Weekly_Sales"].std()),
        "holiday_sales_avg": float(df[df["IsHoliday"] == 1]["Weekly_Sales"].mean())
    }
