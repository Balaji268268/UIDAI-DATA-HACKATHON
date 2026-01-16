
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

def train_forecast_model(df, district_name, periods=180):
    """
    Trains a SARIMA model on the daily enrolment data for a specific district 
    and forecasts the next 'periods' days.
    """
    # Filter for district and Aggregate to Daily series
    district_data = df[df['district'] == district_name].copy()
    daily_series = district_data.groupby('date')['Total_Enrolments'].sum()
    
    # Resample to ensure daily frequency (handle missing days)
    daily_series = daily_series.resample('D').sum().fillna(0)
    
    # Simple Train/Test Split logic (Last 30 days for validation)
    train = daily_series.iloc[:-30]
    test = daily_series.iloc[-30:]

    # Recalibration: Apply Log-Transform to handle non-linear growth and prevent negative predictions
    train_log = np.log1p(train)
    
    # Fit SARIMA on Log-Transformed Data
    # increased MA term to catch sharp spikes
    print(f"Training 'Antigravity' SARIMA model for {district_name} (Log-Scale)...")
    try:
        model = SARIMAX(train_log, order=(1, 1, 2), seasonal_order=(0, 1, 1, 7), enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=False)
    except:
        # Fallback to simpler model if complex one fails
        model = SARIMAX(train_log, order=(1, 1, 0), seasonal_order=(0, 1, 0, 7))
        model_fit = model.fit(disp=False)
    
    # Predict in Log Scale
    forecast_log = model_fit.get_forecast(steps=periods)
    forecast_df = forecast_log.conf_int()
    
    # Inverse Transform (Exp) to return to Real Scale
    forecast_df['Forecast'] = np.expm1(model_fit.predict(start=forecast_log.row_labels[0], end=forecast_log.row_labels[-1]))
    forecast_df.iloc[:, 0] = np.expm1(forecast_df.iloc[:, 0]) # Lower CI
    forecast_df.iloc[:, 1] = np.expm1(forecast_df.iloc[:, 1]) # Upper CI
    
    # Ensure no negative values (Physics enforcement)
    forecast_df[forecast_df < 0] = 0
    
    return daily_series, forecast_df

def run_prediction_engine(enrolment_path, target_districts=None):
    print("Loading Enrolment Data for Forecasting...")
    df = pd.read_csv(enrolment_path, parse_dates=['date'])
    
    if target_districts is None:
        # Default to top 3 busiest districts if not specified
        target_districts = df.groupby('district')['Total_Enrolments'].sum().nlargest(3).index.tolist()
    
    results = {}
    for district in target_districts:
        history, prediction = train_forecast_model(df, district)
        results[district] = {'history': history, 'forecast': prediction}
        print(f"Generated 6-month forecast for {district}")
        
    return results

if __name__ == "__main__":
    # Test run
    results = run_prediction_engine('d:/UIDAI/processed_data/enrolment_clean.csv')
