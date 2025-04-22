import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_data(symbol):
    print(f"Fetching live data for: {symbol}")
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="1m")  # 1-day data with 1-minute granularity
    return data

def save_to_csv(data, symbol="AAPL"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{symbol}_data_{timestamp}.csv"
    data.to_csv(filename)
    print(f"Saved to {filename}")

if __name__ == "__main__":
    symbol = "AAPL"  # you can change this to any stock ticker like "GOOGL", "TSLA", etc.
    data = fetch_stock_data(symbol)
    if not data.empty:
        save_to_csv(data, symbol)
    else:
        print("No data fetched!")
