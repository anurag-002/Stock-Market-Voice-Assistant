import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# Placeholder for Grok API key (replace with actual key)
GROK_API_KEY = "your_grok_api_key_here"
GROK_API_URL = "https://api.x.ai/grok/sentiment"  # Simulated endpoint

# Sample stock lists (simplified; use exchange APIs for full lists)
NSE_STOCKS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "SBIN.NS": "State Bank of India"
}
BSE_STOCKS = {
    "RELIANCE.BO": "Reliance Industries",
    "TCS.BO": "Tata Consultancy Services",
    "HDFCBANK.BO": "HDFC Bank",
    "INFY.BO": "Infosys",
    "SBIN.BO": "State Bank of India"
}
NASDAQ_STOCKS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc."
}

def fetch_stock_data(ticker, period="1y", interval="1d", intraday=False):
    """Fetch historical or intraday stock data."""
    try:
        stock = yf.Ticker(ticker)
        if intraday:
            data = stock.history(period="1d", interval="1m")
        else:
            data = stock.history(period=period, interval=interval)
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        return stock, data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None

def fetch_news(ticker):
    """Fetch recent news for sentiment analysis (simulated)."""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news[:5]
        return [item['title'] for item in news]
    except:
        return []

def grok_sentiment_analysis(text):
    """Simulate Grok API sentiment analysis."""
    try:
        headers = {"Authorization": f"Bearer {GROK_API_KEY}"}
        response = requests.post(GROK_API_URL, json={"text": text}, headers=headers)
        if response.status_code == 200:
            return response.json().get("sentiment", "neutral")
        return "neutral"
    except:
        return "neutral"

# Part 1: Individual Stock Operations
def calculate_moving_average(data, window=20):
    """Calculate simple moving average."""
    return data['Close'].rolling(window=window).mean().iloc[-1]

def calculate_ema(data, window=20):
    """Calculate exponential moving average."""
    return data['Close'].ewm(span=window, adjust=False).mean().iloc[-1]

def calculate_rsi(data, periods=14):
    """Calculate Relative Strength Index."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def calculate_bollinger_bands(data, window=20):
    """Calculate Bollinger Bands."""
    sma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    return sma.iloc[-1], upper.iloc[-1], lower.iloc[-1]

def volume_analysis(data):
    """Analyze trading volume."""
    avg_volume = data['Volume'].mean()
    latest_volume = data['Volume'].iloc[-1]
    return latest_volume, avg_volume, latest_volume / avg_volume if avg_volume else 0

def calculate_pe_ratio(stock):
    """Calculate P/E ratio."""
    try:
        return stock.info.get('trailingPE', np.nan)
    except:
        return np.nan

def calculate_dividend_yield(stock):
    """Calculate dividend yield."""
    try:
        return stock.info.get('dividendYield', 0) * 100
    except:
        return 0

def calculate_beta(stock, market_data, period="1y"):
    """Calculate beta vs market."""
    try:
        stock_data, _ = fetch_stock_data(stock.ticker, period=period)
        stock_returns = stock_data['Close'].pct_change().dropna()
        market_returns = market_data['Close'].pct_change().dropna()
        covariance = stock_returns.cov(market_returns)
        market_variance = market_returns.var()
        return covariance / market_variance if market_variance else np.nan
    except:
        return np.nan

# Part 2: Comparative Operations
def calculate_correlation(data1, data2):
    """Calculate correlation coefficient between two stocks."""
    if len(data1) == len(data2):
        return data1['Close'].corr(data2['Close'])
    return np.nan

def ratio_analysis(data1, data2):
    """Calculate price ratio between two stocks."""
    return data1['Close'].iloc[-1] / data2['Close'].iloc[-1] if data2['Close'].iloc[-1] else np.nan

def spread_analysis(data1, data2):
    """Calculate price spread between two stocks."""
    return data1['Close'].iloc[-1] - data2['Close'].iloc[-1]

def beta_comparison(beta1, beta2):
    """Compare betas of two stocks."""
    return {"Stock1_Beta": beta1, "Stock2_Beta": beta2, "Difference": beta1 - beta2 if beta1 and beta2 else np.nan}

def roi_comparison(data1, data2, period="1y"):
    """Compare ROI of two stocks."""
    roi1 = (data1['Close'].iloc[-1] - data1['Close'].iloc[0]) / data1['Close'].iloc[0] * 100
    roi2 = (data2['Close'].iloc[-1] - data2['Close'].iloc[0]) / data2['Close'].iloc[0] * 100
    return {"Stock1_ROI": roi1, "Stock2_ROI": roi2, "Difference": roi1 - roi2}

def risk_reward_analysis(data1, data2):
    """Compare risk-reward (using standard deviation as risk)."""
    risk1 = data1['Close'].pct_change().std() * np.sqrt(252)
    risk2 = data2['Close'].pct_change().std() * np.sqrt(252)
    return {"Stock1_Risk": risk1, "Stock2_Risk": risk2, "Difference": risk1 - risk2}

def sector_comparison(stock1, stock2):
    """Compare sectors of two stocks."""
    try:
        sector1 = stock1.info.get('sector', 'Unknown')
        sector2 = stock2.info.get('sector', 'Unknown')
        return {"Stock1_Sector": sector1, "Stock2_Sector": sector2, "Same_Sector": sector1 == sector2}
    except:
        return {"Stock1_Sector": "Unknown", "Stock2_Sector": "Unknown", "Same_Sector": False}

def technical_indicator_comparison(data1, data2):
    """Compare technical indicators."""
    rsi1 = calculate_rsi(data1)
    rsi2 = calculate_rsi(data2)
    ma1 = calculate_moving_average(data1)
    ma2 = calculate_moving_average(data2)
    return {
        "RSI": {"Stock1": rsi1, "Stock2": rsi2, "Difference": rsi1 - rsi2 if rsi1 and rsi2 else np.nan},
        "MA": {"Stock1": ma1, "Stock2": ma2, "Difference": ma1 - ma2 if ma1 and ma2 else np.nan}
    }

# Part 3: Additional Operations
def regression_analysis(data):
    """Perform linear regression on stock prices."""
    try:
        X = np.arange(len(data)).reshape(-1, 1)
        y = data['Close'].values
        model = LinearRegression().fit(X, y)
        predicted = model.predict([[len(data)]])[0]
        return {"Slope": model.coef_[0], "Predicted_Next": predicted}
    except:
        return {"Slope": np.nan, "Predicted_Next": np.nan}

def time_series_analysis(data):
    """Perform time series decomposition."""
    try:
        decomposition = seasonal_decompose(data['Close'], model='additive', period=30)
        trend = decomposition.trend.iloc[-1]
        seasonal = decomposition.seasonal.iloc[-1]
        return {"Trend": trend, "Seasonal": seasonal}
    except:
        return {"Trend": np.nan, "Seasonal": np.nan}

def sentiment_analysis(ticker, news):
    """Perform sentiment analysis using VADER and Grok."""
    print("Processing sentiment analysis...")
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = [analyzer.polarity_scores(item)['compound'] for item in news]
    grok_scores = [grok_sentiment_analysis(item) for item in news]
    vader_avg = np.mean(vader_scores) if vader_scores else 0
    grok_sentiment = max(set(grok_scores), key=grok_scores.count) if grok_scores else "neutral"
    return {"VADER_Score": vader_avg, "Grok_Sentiment": grok_sentiment}

def analyze_stock(ticker, market_data):
    """Analyze individual stock."""
    print(f"Processing {ticker} analysis...")
    stock, data = fetch_stock_data(ticker)
    if stock is None or data is None:
        return None
    intraday_stock, intraday_data = fetch_stock_data(ticker, intraday=True)
    news = fetch_news(ticker)
    
    return {
        "Ticker": ticker,
        "Price": data['Close'].iloc[-1],
        "MA": calculate_moving_average(data),
        "EMA": calculate_ema(data),
        "RSI": calculate_rsi(data),
        "Bollinger_Bands": calculate_bollinger_bands(data),
        "Volume": volume_analysis(data),
        "PE_Ratio": calculate_pe_ratio(stock),
        "Dividend_Yield": calculate_dividend_yield(stock),
        "Beta": calculate_beta(stock, market_data),
        "Regression": regression_analysis(data),
        "Time_Series": time_series_analysis(data),
        "Sentiment": sentiment_analysis(ticker, news)
    }

def compare_stocks(ticker1, ticker2, market_data):
    """Compare two stocks."""
    print(f"Processing comparison between {ticker1} and {ticker2}...")
    stock1, data1 = fetch_stock_data(ticker1)
    stock2, data2 = fetch_stock_data(ticker2)
    if stock1 is None or stock2 is None or data1 is None or data2 is None:
        return None
    return {
        "Correlation": calculate_correlation(data1, data2),
        "Price_Ratio": ratio_analysis(data1, data2),
        "Price_Spread": spread_analysis(data1, data2),
        "Beta_Comparison": beta_comparison(
            calculate_beta(stock1, market_data),
            calculate_beta(stock2, market_data)
        ),
        "ROI_Comparison": roi_comparison(data1, data2),
        "Risk_Reward": risk_reward_analysis(data1, data2),
        "Sector_Comparison": sector_comparison(stock1, stock2),
        "Technical_Indicators": technical_indicator_comparison(data1, data2)
    }

def display_stock_lists():
    """Display stock lists for NSE, BSE, NASDAQ."""
    print("\n=== Stock Lists ===")
    print("\nNSE Stocks:")
    for ticker, name in NSE_STOCKS.items():
        print(f"  {ticker}: {name}")
    print("\nBSE Stocks:")
    for ticker, name in BSE_STOCKS.items():
        print(f"  {ticker}: {name}")
    print("\nNASDAQ Stocks:")
    for ticker, name in NASDAQ_STOCKS.items():
        print(f"  {ticker}: {name}")
    print("\nPress Enter to continue...")
    input()

def validate_ticker(ticker):
    """Validate ticker in NSE, BSE, NASDAQ."""
    ticker = ticker.strip().upper()
    # Try NSE (.NS)
    if ticker in NSE_STOCKS or fetch_stock_data(ticker + ".NS")[0] is not None:
        return ticker + ".NS" if not ticker.endswith(".NS") else ticker
    # Try BSE (.BO)
    if ticker in BSE_STOCKS or fetch_stock_data(ticker + ".BO")[0] is not None:
        return ticker + ".BO" if not ticker.endswith(".BO") else ticker
    # Try NASDAQ (no suffix)
    if ticker in NASDAQ_STOCKS or fetch_stock_data(ticker)[0] is not None:
        return ticker
    return None

def individual_operations_menu(ticker, market_data):
    """Menu for individual stock operations."""
    while True:
        print(f"\n=== Individual Operations for {ticker} ===")
        print("1. Moving Average (MA)")
        print("2. Exponential Moving Average (EMA)")
        print("3. Relative Strength Index (RSI)")
        print("4. Bollinger Bands")
        print("5. Volume Analysis")
        print("6. Price-to-Earnings (P/E) Ratio")
        print("7. Dividend Yield")
        print("8. Beta")
        print("9. Back")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            exit()
        if choice == "9":
            return
        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid option. Try again.")
            continue
        
        result = analyze_stock(ticker, market_data)
        if not result:
            print(f"Failed to analyze {ticker}.")
            continue
        
        print(f"\n{ticker} Analysis Result:")
        if choice == "1":
            print(f"Moving Average: {result['MA']}")
        elif choice == "2":
            print(f"EMA: {result['EMA']}")
        elif choice == "3":
            print(f"RSI: {result['RSI']}")
        elif choice == "4":
            print(f"Bollinger Bands: {result['Bollinger_Bands']}")
        elif choice == "5":
            print(f"Volume (Latest, Average, Ratio): {result['Volume']}")
        elif choice == "6":
            print(f"P/E Ratio: {result['PE_Ratio']}")
        elif choice == "7":
            print(f"Dividend Yield: {result['Dividend_Yield']}%")
        elif choice == "8":
            print(f"Beta: {result['Beta']}")
        print("\nPress Enter to continue...")
        input()

def comparative_operations_menu(ticker1, ticker2, market_data):
    """Menu for comparative operations."""
    while True:
        print(f"\n=== Comparative Operations ({ticker1} vs {ticker2}) ===")
        print("1. Correlation Coefficient")
        print("2. Price Ratio")
        print("3. Price Spread")
        print("4. Beta Comparison")
        print("5. ROI Comparison")
        print("6. Risk-Reward Analysis")
        print("7. Sector Comparison")
        print("8. Technical Indicator Comparison")
        print("9. Back")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            exit()
        if choice == "9":
            return
        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid option. Try again.")
            continue
        
        result = compare_stocks(ticker1, ticker2, market_data)
        if not result:
            print(f"Failed to compare {ticker1} and {ticker2}.")
            continue
        
        print(f"\nComparison Result ({ticker1} vs {ticker2}):")
        if choice == "1":
            print(f"Correlation: {result['Correlation']}")
        elif choice == "2":
            print(f"Price Ratio: {result['Price_Ratio']}")
        elif choice == "3":
            print(f"Price Spread: {result['Price_Spread']}")
        elif choice == "4":
            print(f"Beta Comparison: {result['Beta_Comparison']}")
        elif choice == "5":
            print(f"ROI Comparison: {result['ROI_Comparison']}")
        elif choice == "6":
            print(f"Risk-Reward: {result['Risk_Reward']}")
        elif choice == "7":
            print(f"Sector Comparison: {result['Sector_Comparison']}")
        elif choice == "8":
            print(f"Technical Indicators: {result['Technical_Indicators']}")
        print("\nPress Enter to continue...")
        input()

def additional_operations_menu(ticker, market_data):
    """Menu for additional operations."""
    while True:
        print(f"\n=== Additional Operations for {ticker} ===")
        print("1. Regression Analysis")
        print("2. Time Series Analysis")
        print("3. Sentiment Analysis")
        print("4. Back")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            exit()
        if choice == "4":
            return
        if choice not in ["1", "2", "3"]:
            print("Invalid option. Try again.")
            continue
        
        result = analyze_stock(ticker, market_data)
        if not result:
            print(f"Failed to analyze {ticker}.")
            continue
        
        print(f"\n{ticker} Analysis Result:")
        if choice == "1":
            print(f"Regression Analysis: {result['Regression']}")
        elif choice == "2":
            print(f"Time Series Analysis: {result['Time_Series']}")
        elif choice == "3":
            print(f"Sentiment Analysis: {result['Sentiment']}")
        print("\nPress Enter to continue...")
        input()

def main():
    """Main function for menu-driven stock analysis."""
    # Fetch market data for beta calculation
    _, market_data = fetch_stock_data("^GSPC")
    if market_data is None:
        print("Error fetching market data. Exiting.")
        return
    
    while True:
        print("\n=== Stock Analysis System ===")
        print("1. View Stock Lists")
        print("2. Analyze Stocks")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "3":
            print("Goodbye!")
            exit()
        if choice == "1":
            display_stock_lists()
            continue
        if choice != "2":
            print("Invalid option. Try again.")
            continue
        
        # Get and validate first ticker
        while True:
            ticker1 = input("\nEnter first stock ticker (or 'back' to return): ").strip()
            if ticker1.lower() == "back":
                break
            if ticker1.lower() == "exit":
                print("Goodbye!")
                exit()
            validated_ticker1 = validate_ticker(ticker1)
            if validated_ticker1:
                break
            print("Invalid ticker. Please check NSE (.NS), BSE (.BO), or NASDAQ and try again.")
        if ticker1.lower() == "back":
            continue
        
        tickers = [validated_ticker1]
        
        # Ask for second ticker
        while True:
            add_another = input("\nAdd another stock? (y/n): ").strip().lower()
            if add_another == "n":
                break
            if add_another == "y":
                while True:
                    ticker2 = input("Enter second stock ticker (or 'back' to return): ").strip()
                    if ticker2.lower() == "back":
                        break
                    if ticker2.lower() == "exit":
                        print("Goodbye!")
                        exit()
                    validated_ticker2 = validate_ticker(ticker2)
                    if validated_ticker2 and validated_ticker2 != validated_ticker1:
                        tickers.append(validated_ticker2)
                        break
                    print("Invalid or duplicate ticker. Try again.")
                if ticker2.lower() == "back":
                    continue
                break
            print("Please enter 'y' or 'n'.")
        
        # Operations menu
        while True:
            print("\n=== Operations Menu ===")
            print("1. Individual Stock Operations")
            if len(tickers) == 2:
                print("2. Comparative Operations")
            print("3. Additional Operations")
            print("4. Back")
            print("0. Exit")
            choice = input("Select an option: ").strip()
            
            if choice == "0":
                print("Goodbye!")
                exit()
            if choice == "4":
                break
            if choice not in ["1", "2", "3"] or (choice == "2" and len(tickers) != 2):
                print("Invalid option. Try again.")
                continue
            
            if choice == "1":
                for ticker in tickers:
                    individual_operations_menu(ticker, market_data)
            elif choice == "2" and len(tickers) == 2:
                comparative_operations_menu(tickers[0], tickers[1], market_data)
            elif choice == "3":
                for ticker in tickers:
                    additional_operations_menu(ticker, market_data)

if __name__ == "__main__":
    main()
