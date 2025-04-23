# analysis/sentiment.py
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests

def grok_sentiment_analysis(text, api_key, api_url):
    """Simulate Grok API sentiment analysis."""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(api_url, json={"text": text}, headers=headers)
        if response.status_code == 200:
            return response.json().get("sentiment", "neutral")
        return "neutral"
    except:
        return "neutral"

def sentiment_analysis(news, api_key, api_url):
    """Perform sentiment analysis using VADER and Grok."""
    print("Processing sentiment analysis...")
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = [analyzer.polarity_scores(item)['compound'] for item in news]
    grok_scores = [grok_sentiment_analysis(item, api_key, api_url) for item in news]
    vader_avg = np.mean(vader_scores) if vader_scores else 0
    grok_sentiment = max(set(grok_scores), key=grok_scores.count) if grok_scores else "neutral"
    return {"VADER_Score": vader_avg, "Grok_Sentiment": grok_sentiment}
