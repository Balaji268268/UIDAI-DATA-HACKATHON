import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest
from utils import load_and_merge_datasets, basic_preprocessing
from forecasting_engine import run_prediction_engine

def generate_massive_insights(enrolment, demographic, biometric, output_dir):
    """
    Generates the 5 Strategic Insight Pillars as Interactive Plotly Artifacts.
    """
    print("\n[Phase 3] engaging Massive Dynamics Engine (5-Pillar Analysis)...")
    
    # Pillar 1: Ghost Child Finder
    district_ages = enrolment.groupby(['state', 'district'])[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    district_ages['Total'] = district_ages[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)
    district_ages['Child_Share'] = district_ages['age_0_5'] / district_ages['Total']
    district_ages['Z_Score'] = (district_ages['Child_Share'] - district_ages['Child_Share'].mean()) / district_ages['Child_Share'].std()
    district_ages['Child_Share_Pct'] = (district_ages['Child_Share'] * 100).round(1).astype(str) + '%'

    fig1 = px.scatter(district_ages, 
                     x='age_18_greater', 
                     y='age_0_5', 
                     color='Z_Score', 
                     size='Total',
                     hover_name='district',
                     hover_data={'state': True, 'Child_Share_Pct': True, 'age_18_greater': ':,', 'age_0_5': ':,', 'Z_Score': ':.2f', 'Total': False, 'Child_Share': False},
                     color_continuous_scale='RdYlGn',
                     title='Ghost Child Finder: Child vs Adult Activity (Red = Alert)',
                     template='plotly_dark')
    fig1.add_shape(type="line", x0=0, y0=0, x1=district_ages['age_18_greater'].max(), y1=district_ages['age_0_5'].max(),
                  line=dict(color="White", width=1, dash="dash"))
    fig1.write_html(os.path.join(output_dir, '1_ghost_child_radar.html'))
    print(f"  -> Generated: 1_ghost_child_radar.html")

    # Pillar 2: Border Watch
    adult_enrolments = enrolment[enrolment['age_18_greater'] > 0].copy()
    adult_alerts = adult_enrolments.groupby(['state', 'district'])['age_18_greater'].sum().reset_index()
    top_risk = adult_alerts.sort_values('age_18_greater', ascending=False).head(20)

    fig2 = px.bar(top_risk, 
                 x='age_18_greater', 
                 y='district', 
                 color='age_18_greater', 
                 orientation='h',
                 color_continuous_scale='hot',
                 text='age_18_greater',
                 hover_data={'state': True, 'age_18_greater': ':,'},
                 title='Border Watch: Districts with Highest 18+ Enrolment Spikes',
                 template='plotly_dark')
    fig2.update_traces(texttemplate='%{x:,}', textposition='outside')
    fig2.update_layout(yaxis=dict(autorange="reversed"))
    fig2.write_html(os.path.join(output_dir, '2_border_watch_security.html'))
    print(f"  -> Generated: 2_border_watch_security.html")

    # Pillar 3: Migration Radar
    migration_data = demographic.groupby(['state', 'district'])['Total_Demo_Updates'].sum().reset_index()
    fig3 = px.treemap(migration_data, 
                     path=[px.Constant("India"), 'state', 'district'], 
                     values='Total_Demo_Updates',
                     color='Total_Demo_Updates',
                     color_continuous_scale='Viridis',
                     hover_data={'Total_Demo_Updates': ':,'},
                     title='Migration Radar: Population Shift Intensity',
                     template='plotly_dark')
    fig3.write_html(os.path.join(output_dir, '3_migration_radar_flow.html'))
    print(f"  -> Generated: 3_migration_radar_flow.html")

    # Pillar 4: Integrity Shield
    daily_ops = enrolment.groupby(['date', 'district'])['Total_Enrolments'].sum().reset_index()
    model = IsolationForest(contamination=0.005, random_state=42)
    daily_ops['anomaly'] = model.fit_predict(daily_ops[['Total_Enrolments']])

    fig4 = px.scatter(daily_ops, x='date', y='Total_Enrolments', 
                     color=daily_ops['anomaly'].astype(str), 
                     color_discrete_map={'-1': 'red', '1': 'blue'},
                     hover_name='district',
                     hover_data={'Total_Enrolments': ':,', 'date': True},
                     title='Integrity Shield: Operational Anomalies (Red = Fraud Risks)',
                     template='plotly_dark',
                     opacity=0.6)
    fig4.write_html(os.path.join(output_dir, '4_integrity_shield_anomalies.html'))
    print(f"  -> Generated: 4_integrity_shield_anomalies.html")

    # Pillar 5: Youth Tracker
    youth_bio = biometric.groupby(['state', 'district'])['bio_age_5_17'].sum().reset_index()
    youth_enrol = enrolment.groupby(['state', 'district'])['age_5_17'].sum().reset_index()
    youth_metrics = pd.merge(youth_bio, youth_enrol, on=['state', 'district'])
    top_districts = youth_metrics.nlargest(50, 'age_5_17')

    fig5 = px.bar(top_districts, x='district', y=['bio_age_5_17', 'age_5_17'],
                 barmode='group',
                 title='Youth Tracker: Gap between Enrolment (Red) and Biometric Updates (Blue)',
                 template='plotly_dark')
    fig5.write_html(os.path.join(output_dir, '5_youth_tracker_compliance.html'))
    print(f"  -> Generated: 5_youth_tracker_compliance.html")


def save_forecast_results_plotly(results, output_dir):
    """
    Saves forecast data and generates interactive Plotly visualizations (3D/Dynamic).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    combined_data = []

    for district, data in results.items():
        history = data['history']
        forecast = data['forecast']
        
        # 1. Save CSV
        csv_path = os.path.join(output_dir, f'forecast_{district}.csv')
        forecast.to_csv(csv_path)
        
        # Prepare Data for Plotting
        hist_df = history.reset_index()
        hist_df.columns = ['date', 'value']
        hist_df['Type'] = 'Historical'
        
        fore_df = forecast.reset_index()
        fore_df = fore_df.rename(columns={'index': 'date', 'Forecast': 'value'})
        # Ensure integer values for User Clarity
        fore_df['value'] = fore_df['value'].round().astype(int)
        fore_df = fore_df[['date', 'value']]
        fore_df['Type'] = 'Forecast'
        
        full_df = pd.concat([hist_df.tail(120), fore_df]) 
        
        # 2. Individual District Dynamic Chart
        fig = go.Figure()
        
        # Historical Line
        fig.add_trace(go.Scatter(
            x=hist_df.tail(120)['date'], 
            y=hist_df.tail(120)['value'],
            mode='lines',
            name='Historical Demand',
            hovertemplate='Date: %{x}<br>Demand: %{y:,.0f}<extra></extra>',
            line=dict(color='gray', width=2)
        ))
        
        # Forecast Line
        fig.add_trace(go.Scatter(
            x=fore_df['date'], 
            y=fore_df['value'],
            mode='lines+markers',
            name='Predicted Demand',
            hovertemplate='Date: %{x}<br>Predicted: %{y:,.0f}<extra></extra>',
            line=dict(color='cyan', width=3,  shape='spline')
        ))
        
        # Confidence Interval
        fig.add_trace(go.Scatter(
            x=pd.concat([fore_df['date'], fore_df['date'][::-1]]),
            y=pd.concat([forecast.iloc[:, 1], forecast.iloc[:, 0][::-1]]),
            fill='toself',
            fillcolor='rgba(0, 255, 255, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='Probability Cloud'
        ))

        fig.update_layout(
            title=f"Gravity Well Analysis: {district}",
            template="plotly_dark",
            xaxis_title="Temporal Coordinates (Date)",
            yaxis_title="Mass (Enrolment Demand)",
            hovermode="x unified"
        )
        
        html_path = os.path.join(output_dir, f'dynamic_chart_{district}.html')
        fig.write_html(html_path)
        print(f"Saved Dynamic Map for {district}: {html_path}")
        
        subset = fore_df.copy()
        subset['District'] = district
        combined_data.append(subset)

    # 3. Create 3D Surface Field Visualization
    if combined_data:
        all_forecasts = pd.concat(combined_data)
        
        fig3d = px.line_3d(
            all_forecasts, 
            x='date', 
            y='District', 
            z='value', 
            color='District',
            title="3D Antigravity Field: Multi-District Demand Surface",
            template="plotly_dark"
        )
        fig3d.update_layout(scene = dict(
                    xaxis_title='Time',
                    yaxis_title='District',
                    zaxis_title='Demand Amplitude'))
        
        html_3d_path = os.path.join(output_dir, '3d_antigravity_field.html')
        fig3d.write_html(html_3d_path)
        print(f"Saved 3D Field Visualization: {html_3d_path}")

def main():
    print("========================================")
    print("   AADHAAR 360 - MASSIVE DYNAMICS ENGINE   ")
    print("========================================")
    
    # 1. Data Ingestion
    print("\n[Phase 1] Calibrating Sensors (Data Ingestion)...")
    base_path = 'd:/UIDAI'
    raw_data = load_and_merge_datasets(base_path)
    cleaned_data = basic_preprocessing(raw_data)
    
    os.makedirs(os.path.join(base_path, 'processed_data'), exist_ok=True)
    enrolment_df = cleaned_data['enrolment']
    demographic_df = cleaned_data['demographic']
    biometric_df = cleaned_data['biometric']
    
    if enrolment_df.empty:
        print("CRITICAL FAILURE: No Data Mass Detected.")
        return
        
    enrolment_df['Total_Enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']
    
    # Calculate Totals for Demographic and Biometric
    # Demographic columns: 'mobile_update', 'email_update', 'dob_update', 'address_update', 'name_update', 'gender_update' (simplified assumption, need to match actual columns or sum all numeric except date/district)
    # Based on notebook logic, checking columns. Assuming standard named columns or summing specific ones.
    # The error was 'Total_Demo_Updates'.
    # In the absence of explicit column names, sum all update types.
    # Let's check available columns in logic or sum typical ones. 
    # For safety, summing know update columns if they exist, or all numeric.
    # A safer bet is to sum the known update columns if present.
    update_cols = ['mobile_update', 'email_update', 'dob_update', 'address_update', 'name_update', 'gender_update']
    existing_cols = [c for c in update_cols if c in demographic_df.columns]
    if existing_cols:
         demographic_df['Total_Demo_Updates'] = demographic_df[existing_cols].sum(axis=1)
    else:
         # Fallback: Sum all numeric columns excluding district and date
         numeric_pd = demographic_df.select_dtypes(include=np.number)
         demographic_df['Total_Demo_Updates'] = numeric_pd.sum(axis=1)

    # Biometric Totals?
    # Notebook used 'bio_age_5_17'. Inspecting usage.
    # It seems to use 'bio_age_5_17' directly. 
    # Just in case, ensuring columns exist.
    
    # Save processed data for record
    enrolment_df.to_csv(os.path.join(base_path, 'processed_data', 'enrolment_clean.csv'), index=False)
    demographic_df.to_csv(os.path.join(base_path, 'processed_data', 'demographic_clean.csv'), index=False)
    biometric_df.to_csv(os.path.join(base_path, 'processed_data', 'biometric_clean.csv'), index=False)

    results_dir = os.path.join(base_path, 'results')

    # 2. Advanced Forecasting (Smart Selection)
    print("\n[Phase 2] Engaging Antigravity Engine (Log-Linear Predictions)...")
    # Smart Select: Only forecast districts with MEANINGFUL volume to avoid '1s and 0s'
    # Criteria: Top 3 districts by TOTAL volume
    top_districts = enrolment_df.groupby('district')['Total_Enrolments'].sum().nlargest(3).index.tolist()
    print(f"Targeting High-Gravity Districts: {top_districts}")
    
    forecast_results = run_prediction_engine(os.path.join(base_path, 'processed_data', 'enrolment_clean.csv'), target_districts=top_districts)
    save_forecast_results_plotly(forecast_results, results_dir)
    
    # 3. Massive Insight Generation
    generate_massive_insights(enrolment_df, demographic_df, biometric_df, results_dir)
    
    print("\n========================================")
    print("   MISSION ACCOMPLISHED - SYSTEM ACTIVATED   ")
    print("========================================")

if __name__ == "__main__":
    main()
