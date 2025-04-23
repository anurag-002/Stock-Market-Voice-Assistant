from fastapi import FastAPI
from analysis.indicators import calculate_rsi, calculate_moving_average
from analysis.sentiment import get_sentiment_score
from analysis.comparison import roi_comparison, technical_indicator_comparison
from utils.fetch import fetch_stock_data
import json

app = FastAPI()

# Sample endpoint to fetch stock data
@app.get("/stock/{ticker}")
async def get_stock_data(ticker: str):
    try:
        stock_data = fetch_stock_data(ticker)
        return {"ticker": ticker, "data": stock_data.to_dict()}
    except Exception as e:
        return {"error": f"Failed to fetch stock data: {str(e)}"}

# Endpoint for sentiment analysis
@app.get("/sentiment/{ticker}")
async def get_stock_sentiment(ticker: str):
    try:
        stock_data = fetch_stock_data(ticker)
        sentiment_score = get_sentiment_score(stock_data)
        return {"ticker": ticker, "sentiment_score": sentiment_score}
    except Exception as e:
        return {"error": f"Failed to fetch sentiment: {str(e)}"}

# Endpoint for technical indicators comparison
@app.get("/indicators/{ticker}")
async def get_indicators(ticker: str):
    try:
        stock_data = fetch_stock_data(ticker)
        rsi = calculate_rsi(stock_data)
        ma = calculate_moving_average(stock_data)
        return {"ticker": ticker, "RSI": rsi, "MA": ma}
    except Exception as e:
        return {"error": f"Failed to fetch indicators: {str(e)}"}

# Endpoint for stock comparison
@app.get("/compare/{ticker1}/{ticker2}")
async def compare_stocks(ticker1: str, ticker2: str):
    try:
        stock_data1 = fetch_stock_data(ticker1)
        stock_data2 = fetch_stock_data(ticker2)
        
        comparison = technical_indicator_comparison(stock_data1, stock_data2)
        roi = roi_comparison(stock_data1, stock_data2)
        
        return {"comparison": comparison, "roi": roi}
    except Exception as e:
        return {"error": f"Failed to compare stocks: {str(e)}"}
