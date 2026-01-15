import pandas as pd
import os
import glob
from pathlib import Path

def load_and_merge_datasets(base_path):
    """
    Loads and merges split CSV files from the Aadhaar Enrolment, Demographic, and Biometric directories.
    
    Args:
        base_path (str): The root directory containing the dataset folders (e.g., 'd:/UIDAI').
        
    Returns:
        dict: A dictionary containing three DataFrames: 'enrolment', 'biometric', 'demographic'.
    """
    
    datasets = {
        'enrolment': {'folder': 'api_data_aadhar_enrolment', 'pattern': '*.csv'},
        'demographic': {'folder': 'api_data_aadhar_demographic', 'pattern': '*.csv'},
        'biometric': {'folder': 'api_data_aadhar_biometric', 'pattern': '*.csv'}
    }
    
    loaded_data = {}
    
    for key, config in datasets.items():
        folder_path = os.path.join(base_path, config['folder'])
        search_pattern = os.path.join(folder_path, config['pattern'])
        files = glob.glob(search_pattern)
        
        if not files:
            print(f"Warning: No files found for {key} in {folder_path}")
            loaded_data[key] = pd.DataFrame()
            continue
            
        print(f"Loading {len(files)} files for {key}...")
        df_list = []
        for file in files:
            try:
                # Read CSV - enforcing string for pincode to preserve leading zeros
                df = pd.read_csv(file, dtype={'pincode': str})
                
                # Standardize column names (lowercase, strip whitespace)
                df.columns = df.columns.str.lower().str.strip()
                
                # Convert 'date' to datetime immediately to ensure consistency
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
                
                df_list.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        if df_list:
            merged_df = pd.concat(df_list, ignore_index=True)
            loaded_data[key] = merged_df
            print(f"Successfully merged {key}: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns.")
        else:
            loaded_data[key] = pd.DataFrame()
            
    return loaded_data

def basic_preprocessing(dfs):
    """
    Performs initial standard preprocessing on the loaded DataFrames.
    """
    cleaned_dfs = {}
    
    for key, df in dfs.items():
        if df.empty:
            cleaned_dfs[key] = df
            continue
            
        # Drop duplicates if any
        df = df.drop_duplicates()
        
        # Ensure pincode is cleaned (remove non-numeric characters if any)
        if 'pincode' in df.columns:
            df['pincode'] = df['pincode'].str.replace(r'\D', '', regex=True)
            
        # Basic imputation: Fill NaNs in count columns with 0
        # numeric_cols = df.select_dtypes(include=['number']).columns
        # df[numeric_cols] = df[numeric_cols].fillna(0)
        
        cleaned_dfs[key] = df
        print(f"Preprocessing completed for {key}.")
        
    return cleaned_dfs
