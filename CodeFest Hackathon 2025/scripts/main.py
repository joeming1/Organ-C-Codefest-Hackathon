import pandas as pd

# -----------------------------
# 1️⃣ Load and preprocess data
# -----------------------------
df = pd.read_csv("CodeFest Hackathon 2025/csv/forecast_stores.csv")

# Ensure numeric yhat
df['yhat'] = df['yhat'].astype(float)

# Convert dates
df['ds'] = pd.to_datetime(df['ds'])

# Sort by store and date
df = df.sort_values(['Store', 'ds'])

# -----------------------------
# 2️⃣ Calculate metrics
# -----------------------------
# Percent change (week-to-week)
df['yhat_change_pct'] = df.groupby('Store')['yhat'].pct_change() * 100

# Rolling volatility (3-week window)
df['volatility'] = df.groupby('Store')['yhat'].rolling(3).std().reset_index(0, drop=True)

# -----------------------------
# 3️⃣ Anomaly detection
# -----------------------------
yhat_drop_threshold = -5
yhat_spike_threshold = 5
volatility_pct_threshold = 0.05  # 5% of yhat

df['anomaly'] = (
    (df['yhat_change_pct'].abs() > max(abs(yhat_drop_threshold), yhat_spike_threshold)) |
    (df.groupby('Store')['yhat_change_pct'].transform(lambda x: x.abs().quantile(0.95)) <= df['yhat_change_pct'].abs())
)

# -----------------------------
# 4️⃣ Risk score
# -----------------------------
df['risk_score'] = df['yhat_change_pct'].abs() + (df['volatility'] / df['yhat']) * 100

# Optional: classify risk level
def classify_risk(score):
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"

df['risk_level'] = df['risk_score'].apply(classify_risk)

# -----------------------------
# 5️⃣ Dynamic thresholds per store
# -----------------------------
# Calculate 10th and 90th percentiles per store
percentiles = df.groupby('Store')['yhat'].quantile([0.10, 0.90]).unstack()
percentiles.columns = ['low_sales_threshold', 'high_sales_threshold']

# Merge thresholds back to df
df = df.merge(percentiles, left_on='Store', right_index=True)

# -----------------------------
# 6️⃣ Final Action & Reason (with Normal Range in Millions)
# -----------------------------
def action_reason(row):
    if pd.isna(row['yhat_change_pct']):
        return pd.Series([
            'No Action',
            'First week or insufficient historical data to assess change.'
        ])
    
    # Large drop
    if row['yhat_change_pct'] < yhat_drop_threshold:
        return pd.Series([
            'Investigate / Promote',
            f'Sales predicted to drop by {abs(row["yhat_change_pct"]):.1f}% compared to last week. Consider marketing actions or promotions.'
        ])
    
    # Large spike
    elif row['yhat_change_pct'] > yhat_spike_threshold:
        return pd.Series([
            'Prepare Inventory',
            f'Sales predicted to increase by {row["yhat_change_pct"]:.1f}% compared to last week. Ensure sufficient stock.'
        ])
    
    # High volatility
    elif row['volatility'] > volatility_pct_threshold * row['yhat']:
        return pd.Series([
            'Monitor Closely',
            f'Sales forecast shows high week-to-week volatility. Watch inventory and marketing closely.'
        ])
    
    # Low forecasted sales
    elif row['yhat'] < row['low_sales_threshold']:
        return pd.Series([
            'Review Marketing',
            f'Forecasted weekly sales ({row["yhat"]/1_000_000:.2f}M) are below this store’s normal range '
            f'({row["low_sales_threshold"]/1_000_000:.2f}M–{row["high_sales_threshold"]/1_000_000:.2f}M). Consider promotions or cost management.'
        ])
    
    # High forecasted sales
    elif row['yhat'] > row['high_sales_threshold']:
        return pd.Series([
            'Prepare Inventory',
            f'Forecasted weekly sales ({row["yhat"]/1_000_000:.2f}M) exceed this store’s normal range '
            f'({row["low_sales_threshold"]/1_000_000:.2f}M–{row["high_sales_threshold"]/1_000_000:.2f}M). Ensure stock and logistics are ready.'
        ])
    
    # Anomaly detected
    elif row['anomaly']:
        return pd.Series([
            'Investigate Anomaly',
            'Week shows unusual sales change compared to historical patterns.'
        ])
    
    # Normal forecast
    else:
        return pd.Series([
            'No Action',
            f'Forecast is normal. Expected weekly sales are within the store’s normal range '
            f'({row["low_sales_threshold"]/1_000_000:.2f}M–{row["high_sales_threshold"]/1_000_000:.2f}M).'
        ])

# Apply the function
df[['action', 'reason']] = df.apply(action_reason, axis=1)

# -----------------------------
# 7️⃣ Save output
# -----------------------------
df.to_csv("CodeFest Hackathon 2025/outputs/forecast_analysis_weekly_dashboard.csv", index=False)
print("✅ CSV ready for dashboard: forecast_analysis_weekly_dashboard.csv")



