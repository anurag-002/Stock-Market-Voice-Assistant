# analysis/comparison.py

from analysis.indicators import calculate_rsi, calculate_moving_average
import numpy as np


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
