# utils/fetch.py

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch historical stock data using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        if data.empty:
            raise ValueError("No data returned for ticker")
        return data
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return pd.DataFrame()


def fetch_news(ticker):
    """
    Fetch recent news articles for a stock ticker (placeholder).
    """
    # Placeholder: replace with real API like NewsAPI, Finnhub, etc.
    return [
        {"title": f"Latest news about {ticker}", "source": "MockNews", "url": "https://example.com"},
        {"title": f"{ticker} hits new high!", "source": "MockFinance", "url": "https://example.com"}
    ]
