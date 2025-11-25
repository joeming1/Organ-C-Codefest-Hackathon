import pandas as pd
from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Walmart_Sales.csv"

@lru_cache(maxsize=1)
def load_raw_data() -> pd.DataFrame:
    print("Loading CSV from:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)

    # FIX: Correct datetime parsing
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")

    return df

def get_time_series(store_id: int | None = None) -> pd.DataFrame:
    df = load_raw_data()

    if store_id is not None:
        df = df[df["Store"] == store_id]
    else:
        df = df.groupby("Date", as_index=False)["Weekly_Sales"].sum()

    df = df.rename(columns={"Date": "timestamp", "Weekly_Sales": "value"})
    df = df.sort_values("timestamp")

    return df[["timestamp", "value"]]
