def generate_summary(ticker, data_list):
    """
    Generates a natural language summary based on technical indicators.
    """
    if not data_list or len(data_list) < 2:
        return f"Not enough data to generate a summary for {ticker}."
    
    latest = data_list[-1]
    prev = data_list[-2]
    
    summary_parts = []
    
    # price movement
    price_change = latest['Close'] - prev['Close']
    direction = "bullish" if price_change > 0 else "bearish"
    summary_parts.append(f"{ticker} is showing {direction} momentum today.")
    
    # RSI
    rsi = latest.get('RSI')
    if rsi is not None:
        if rsi > 70:
            summary_parts.append(f"The RSI is at {rsi:.1f}, indicating the stock might be overbought.")
        elif rsi < 30:
            summary_parts.append(f"The RSI is at {rsi:.1f}, suggesting the stock could be oversold.")
        else:
            summary_parts.append(f"The RSI is neutral at {rsi:.1f}.")

    # MA
    sma50 = latest.get('SMA_50')
    sma200 = latest.get('SMA_200')
    current_price = latest.get('Close')

    if sma50 and current_price:
        if current_price > sma50:
            summary_parts.append("The price is currently trading above its 50-day moving average, a positive signal.")
        else:
            summary_parts.append("The price is below the 50-day moving average.")
            
    if sma50 and sma200:
        if sma50 > sma200:
            summary_parts.append("A Golden Cross pattern (50-day > 200-day) is present, suggesting long-term upside.")
        elif sma50 < sma200:
            summary_parts.append("A Death Cross pattern (50-day < 200-day) is visible, indicating potential long-term downside.")

    return " ".join(summary_parts)
