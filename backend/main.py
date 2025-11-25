from fastapi import FastAPI
from routes.forecast import router as forecast_router
from routes.anomaly import router as anomaly_router
from routes.kpi import router as kpi_router
from routes.risk import router as risk_router
from routes.alerts import router as alerts_router
from routes.cluster import router as cluster_router



app = FastAPI(
    title="Enterprise Predictive Analytics API",
    version="1.0.0",
    description="Track 1: Intelligent Predictive Analytics using Walmart Sales data"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(cluster_router, prefix="/cluster", tags=["KMeans"])
app.include_router(forecast_router, prefix="/forecast", tags=["Forecast"])
app.include_router(anomaly_router, prefix="/anomaly", tags=["Anomaly Detection"])
app.include_router(kpi_router, prefix="/kpi", tags=["KPI Overview"])
app.include_router(risk_router, prefix="/risk", tags=["Risk Level"])
app.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
