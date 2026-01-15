import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_and_merge_datasets, basic_preprocessing
from forecasting_engine import run_prediction_engine

def save_forecast_results(results, output_dir):
    """
    Saves forecast data to CSV and generates plots.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for district, data in results.items():
        history = data['history']
        forecast = data['forecast']
        
        # 1. Save CSV
        csv_path = os.path.join(output_dir, f'forecast_{district}.csv')
        forecast.to_csv(csv_path)
        
        # 2. Generate Plot
        plt.figure(figsize=(12, 6))
        
        # Plot last 90 days of history for context
        plt.plot(history.index[-90:], history.values[-90:], label='Historical Data (Last 90 Days)')
        
        # Plot Forecast
        plt.plot(forecast.index, forecast['Forecast'], label='Predicted Demand', color='orange')
        
        # Plot Confidence Intervals
        plt.fill_between(forecast.index, 
                         forecast.iloc[:, 0], # Lower CI
                         forecast.iloc[:, 1], # Upper CI
                         color='orange', alpha=0.2, label='95% Confidence Interval')
        
        plt.title(f"Aadhaar AI Forecast: {district} (Next 6 Months)")
        plt.xlabel("Date")
        plt.ylabel("Enrolment Demand")
        plt.legend()
        plt.grid(True)
        
        # Save Plot
        plot_path = os.path.join(output_dir, f'forecast_chart_{district}.png')
        plt.savefig(plot_path)
        plt.close()
        
        print(f"Saved results for {district}: {csv_path}, {plot_path}")

def main():
    print("========================================")
    print("   AADHAAR 360 - INTELLIGENCE GRID      ")
    print("========================================")
    
    # 1. Data Ingestion & Cleaning
    print("\n[Phase 1] Data Ingestion & Preprocessing...")
    base_path = 'd:/UIDAI'
    raw_data = load_and_merge_datasets(base_path)
    cleaned_data = basic_preprocessing(raw_data)
    
    # Save Pipeline
    os.makedirs(os.path.join(base_path, 'processed_data'), exist_ok=True)
    
    enrolment_df = cleaned_data['enrolment']
    if not enrolment_df.empty:
        enrolment_df['Total_Enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']
        save_path = os.path.join(base_path, 'processed_data', 'enrolment_clean.csv')
        enrolment_df.to_csv(save_path, index=False)
        print(f"Verified Data: Saved Clean Enrolment Data to {save_path}")
    else:
        print("CRITICAL ERROR: No Enrolment Data Found. Cannot proceed to forecasting.")
        return

    # 2. Advanced Forecasting
    print("\n[Phase 2] Running Time-Traveler Module (SARIMA Forecasting)...")
    forecast_results = run_prediction_engine(save_path)
    
    # 3. Saving Results
    print("\n[Phase 3] Visualizing & Saving Results...")
    results_dir = os.path.join(base_path, 'results')
    save_forecast_results(forecast_results, results_dir)
    
    print("\n========================================")
    print("   ANALYSIS COMPLETE - CHECK 'results' FOLDER   ")
    print("========================================")

if __name__ == "__main__":
    main()
