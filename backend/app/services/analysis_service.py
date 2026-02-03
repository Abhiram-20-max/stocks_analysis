import pandas as pd
import numpy as np

def calculate_technical_indicators(data_list):
    """
    Calculates SMA_50, SMA_200, RSI, MACD.
    Expects data_list to be a list of dicts (from data_service).
    Returns list of dicts with added indicators.
    """
    if not data_list:
        return []
        
    df = pd.DataFrame(data_list)
    
    # Ensure sorted by date
    df.sort_values('Date', inplace=True)
    
    # Calculate simple moving averages
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate MACD
    # EMA 12
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    # EMA 26
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    
    df['MACD'] = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Fill NaN with None for JSON compliance
    df = df.where(pd.notnull(df), None)
    
    return df.to_dict(orient='records')
