
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
    
    # Fit SARIMA (Simple order for speed, can be optimized)
    # Order: (p,d,q) = (1,1,1), Seasonal Order: (1,1,1,7) [Weekly seasonality]
    print(f"Training SARIMA model for {district_name}...")
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
    model_fit = model.fit(disp=False)
    
    # Predict
    forecast = model_fit.get_forecast(steps=periods)
    forecast_df = forecast.conf_int()
    forecast_df['Forecast'] = model_fit.predict(start=forecast.row_labels[0], end=forecast.row_labels[-1])
    
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
