def calculate_risk(anomalies_count, volatility):
    if anomalies_count > 5 or volatility > 0.2:
        return "HIGH"
    if anomalies_count > 2:
        return "MEDIUM"
    return "LOW"
