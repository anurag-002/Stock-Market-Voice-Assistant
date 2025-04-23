# analysis/forecast.py
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np

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
