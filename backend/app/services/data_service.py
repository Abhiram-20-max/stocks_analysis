import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    """
    Fetches historical stock data for the given ticker.
    Returns a dictionary with historical data (records) and info.
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get 1 year of data
        hist = stock.history(period="1y")
        
        if hist.empty:
            return None
        
        # Reset index to make Date a column
        hist.reset_index(inplace=True)
        
        # Convert Date to string for JSON serialization
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        
        # Clean data: drop NAs
        hist.dropna(inplace=True)
        
        # Get basics
        info = stock.info
        
        return {
            "history": hist.to_dict(orient='records'),
            "info": {
                "shortName": info.get("shortName", ticker),
                "sector": info.get("sector", "Unknown"),
                "summaryQuote": info.get("currentPrice", 0), # Fallback if needed
                "peRatio": info.get("trailingPE", None),
                "earningsGrowth": info.get("earningsGrowth", None),
                "currency": info.get("currency", "USD")
            }
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
