from voice.speech_to_text import convert_speech_to_text
from voice.text_to_speech import speak_text
from voice.ai_integration import groq_ticker_resolution
from utils.validate import validate_ticker
from utils.fetch import fetch_stock_data
from analysis.sentiment import analyze_sentiment
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
from analysis.forecast import forecast_stock_price
from fluvio_streaming.producer import produce_stock_data


def main():
    speak_text("Voice assistant activated. How can I help you today?")
    while True:
        user_input = convert_speech_to_text()

        if "exit" in user_input.lower():
            speak_text("Goodbye!")
            break

        resolved_ticker = groq_ticker_resolution(user_input)
        ticker = validate_ticker(resolved_ticker)

        if not ticker:
            speak_text("Sorry, I couldn't recognize that stock ticker.")
            continue

        stock_data = fetch_stock_data(ticker)
        produce_stock_data(ticker, stock_data)

        sentiment = analyze_sentiment(ticker)
        speak_text(f"The current sentiment for {ticker} is {sentiment}.")

        forecast = forecast_stock_price(ticker)
        speak_text(f"The forecasted price for {ticker} is {forecast:.2f}.")


if __name__ == "__main__":
    main()
