def get_kpi_overview(df):
    return {
        "mean": float(df["value"].mean()),
        "std_dev": float(df["value"].std()),
        "min": float(df["value"].min()),
        "max": float(df["value"].max()),
        "volatility": float(df["value"].std() / df["value"].mean()),
        "latest_value": float(df["value"].iloc[-1]),
        "trend": "up" if df["value"].iloc[-1] > df["value"].iloc[-2] else "down"
    }
