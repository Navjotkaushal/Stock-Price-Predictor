# Data Ingestion layer

import yfinance as yf 
import pandas as pd 
import sqlite3 
from datetime import datetime 
import time 

TICKER = "TSLA"
DB_NAME = "stock_db"
TABLE_NAME = "stoc_prices"
INTERVAL = "1d"
PERIOD = "7d"


conn = sqlite3.connect(DB_NAME )

# Initial Loading 
def initial_load():
    print("Running initial data loading...")
    
    df = yf.download(TICKER, interval=INTERVAL, period=PERIOD)
    df.reset_index(inplace=True)
    
    df = clean_data(df)
    
    df.to_sql(TABLE_NAME, conn, if_exists = "replace", index = False)
    
# Cleaning data 

def clean_data(df):
    df.rename(columns={'Datetime':'Date'}, inplace = True)
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    num_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df.dropna(inplace = True)
    
    return df 

# getting last timestamp 
def get_last_timestamp():
    try:
        query = f"SELECT MAX(Date) as Last_date From {TABLE_NAME}"
        result = pd.read_sql(query, conn)
        
        return result['Last_date'][0]
    except:
        return None 
        
        
def incremental_update():
    print("Checking for new data...")

    last_timestamp = get_last_timestamp()

    new_data = yf.download(TICKER, interval=INTERVAL, period=PERIOD)
    new_data.reset_index(inplace=True)

    new_data = clean_data(new_data)

    if last_timestamp:
        new_data = new_data[new_data['Date'] > last_timestamp]

    if not new_data.empty:
        new_data.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        print(f"Added {len(new_data)} new rows.")
    else:
        print("No new data.")

def get_latest_data(n=100):
    query = f"""
    SELECT * FROM {TABLE_NAME}
    ORDER BY Date DESC
    LIMIT {n}
    """
    df = pd.read_sql(query, conn)
    return df.sort_values(by="Date")

if __name__ == "__main__":

    # First time run
    if get_last_timestamp() is None:
        initial_load()

    # Run continuous updates
    while True:
        incremental_update()

        # Example: fetch latest data for ML
        latest_df = get_latest_data(50)
        print("Latest data shape:", latest_df.shape)

        # Wait 5 minutes
        time.sleep(300)