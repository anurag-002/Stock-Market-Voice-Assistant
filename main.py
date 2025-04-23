from voice.speech_to_text import convert_speech_to_text
from voice.text_to_speech import speak
from voice.ai_integration import groq_ticker_resolution
from utils.validate import validate_ticker
from utils.fetch import fetch_stock_data
from analysis.sentiment import sentiment_analysis
from analysis.comparison import (
    calculate_correlation,
    ratio_analysis,
    spread_analysis,
    beta_comparison,
    roi_comparison,
    risk_reward_analysis,
    sector_comparison,
    technical_indicator_comparison,
)
from analysis.forecast import time_series_analysis, regression_analysis
from fluvio_streaming.producer import produce_stock_data


def main():
    speak("Voice assistant activated. How can I help you today?")
    while True:
        user_input = convert_speech_to_text()

        if "exit" in user_input.lower():
            speak("Goodbye!")
            break

        resolved_ticker = groq_ticker_resolution(user_input)
        ticker = validate_ticker(resolved_ticker)

        if not ticker:
            speak("Sorry, I couldn't recognize that stock ticker.")
            continue

        stock_data = fetch_stock_data(ticker)
        produce_stock_data(ticker, stock_data)

        sentiment = sentiment_analysis(ticker)
        speak(f"The current sentiment for {ticker} is {sentiment}.")

        forecast = regression_analysis(ticker)
        speak(f"The forecasted price for {ticker} is {forecast:.2f}.")


if __name__ == "__main__":
    main()
