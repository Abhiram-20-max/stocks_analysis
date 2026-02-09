import os
import yfinance as yf
import pandas as pd
import requests

def get_stock_data(ticker):
    """
    Fetches historical stock data for the given ticker.
    Returns a dictionary with historical data (records) and info.
    """
    data = _fetch_yahoo(ticker)
    if data is not None:
        return data

    api_key = _get_alpha_vantage_key()
    if api_key:
        data = _fetch_alpha_vantage(ticker, api_key)
        if data is None:
            print(f"Alpha Vantage fallback failed for {ticker}.")
        return data

    print("Alpha Vantage API key not set; cannot use fallback provider.")

    return None


def _get_alpha_vantage_key():
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if api_key:
        return api_key

    env_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
    ]

    for env_path in env_paths:
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as env_file:
                for raw_line in env_file:
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    if key.strip() == "ALPHAVANTAGE_API_KEY":
                        api_key = value.strip().strip('"')
                        if api_key:
                            os.environ["ALPHAVANTAGE_API_KEY"] = api_key
                            return api_key
        except Exception as e:
            print(f"Failed to read .env for Alpha Vantage key: {e}")

    return None


def _fetch_yahoo(ticker):
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
                "summaryQuote": info.get("currentPrice", 0),
                "peRatio": info.get("trailingPE", None),
                "earningsGrowth": info.get("earningsGrowth", None),
                "currency": info.get("currency", "USD")
            }
        }
    except Exception as e:
        print(f"Error fetching Yahoo data for {ticker}: {e}")
        return None


def _fetch_alpha_vantage(ticker, api_key):
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY&symbol={ticker}"
            f"&outputsize=compact&apikey={api_key}"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        payload = response.json()

        series = payload.get("Time Series (Daily)")
        if not series:
            print(
                f"Alpha Vantage error for {ticker}: "
                f"{payload.get('Note') or payload.get('Information') or payload.get('Error Message')}"
            )
            return None

        df = pd.DataFrame.from_dict(series, orient="index")
        df.index.name = "Date"
        df.reset_index(inplace=True)

        rename_map = {
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }
        df.rename(columns=rename_map, inplace=True)
        df["Adj Close"] = df["Close"]
        df = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

        # Convert types
        for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df.dropna(inplace=True)

        # Keep last year of data
        cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=365)
        df = df[df["Date"] >= cutoff]
        df.sort_values("Date", inplace=True)

        df["Date"] = df["Date"].dt.strftime('%Y-%m-%d')

        return {
            "history": df.to_dict(orient='records'),
            "info": {
                "shortName": ticker,
                "sector": "Unknown",
                "summaryQuote": float(df.iloc[-1]["Close"]) if not df.empty else 0,
                "peRatio": None,
                "earningsGrowth": None,
                "currency": "USD"
            }
        }
    except Exception as e:
        print(f"Error fetching Alpha Vantage data for {ticker}: {e}")
        return None
