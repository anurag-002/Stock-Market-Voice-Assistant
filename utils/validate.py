# utils/validate.py
import yfinance as yf
import logging

# For AI resolution using Groq
from voice.ai_integration import groq_ticker_resolution

def is_valid_ticker(ticker):
    """Check if the ticker symbol is valid using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        if "symbol" in stock_info:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error in ticker validation: {e}")
        return False

def get_ticker_info(ticker):
    """Fetch basic information of a ticker using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception as e:
        logging.error(f"Error fetching ticker info: {e}")
        return None

def resolve_ticker(ticker):
    """Try to resolve the ticker using Groq for better AI-powered resolution."""
    try:
        # Attempt AI resolution using Groq (if Groq is available)
        resolved_ticker = groq_ticker_resolution(ticker)
        if resolved_ticker:
            return resolved_ticker
        else:
            return None
    except Exception as e:
        logging.error(f"AI resolution failed: {e}")
        return None

def validate_ticker(ticker):
    """Check if ticker is valid, and resolve if necessary."""
    if is_valid_ticker(ticker):
        return ticker
    else:
        logging.warning(f"Ticker {ticker} is invalid. Attempting AI resolution...")
        resolved_ticker = resolve_ticker(ticker)
        if resolved_ticker:
            return resolved_ticker
        else:
            logging.error(f"Could not resolve ticker {ticker}.")
            return None
