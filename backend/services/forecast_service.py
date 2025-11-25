import pandas as pd
from prophet import Prophet

def forecast_kpi(df, periods=7):
    df = df.rename(columns={"timestamp": "ds", "value": "y"})

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
