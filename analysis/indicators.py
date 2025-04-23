# analysis/indicators.py

import numpy as np

def calculate_moving_average(data, window=20):
    return data['Close'].rolling(window=window).mean().iloc[-1]

def calculate_ema(data, window=20):
    return data['Close'].ewm(span=window, adjust=False).mean().iloc[-1]

def calculate_rsi(data, periods=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def calculate_bollinger_bands(data, window=20):
    sma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    return sma.iloc[-1], upper.iloc[-1], lower.iloc[-1]
