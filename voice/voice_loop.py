import time
import speech_to_text
import text_to_speech
from utils.fetch import fetch_stock_data
from voice.ai_integration import groq_ticker_resolution  # Updated import

def start_conversation():
    # Greeting message when assistant starts
    text_to_speech.speak("Voice assistant activated. How can I help you today?")
    
    while True:
        user_input = speech_to_text.convert_speech_to_text()  # Capture voice input
        
        if user_input:
            user_input = user_input.lower()  # Normalize input to lowercase
            print(f"User said: {user_input}")
            
            # Stock-related queries
            if "stock price" in user_input or "price" in user_input:
                # Use Groq to resolve ticker from the voice input
                ticker = groq_ticker_resolution(user_input)
                
                if ticker:
                    # Fetch stock data using the resolved ticker
                    stock_data = fetch_stock_data(ticker)
                    
                    if stock_data is not None:
                        price = stock_data['Close'].iloc[-1]
                        text_to_speech.speak(f"The current price of {ticker.upper()} is {price}")
                    else:
                        text_to_speech.speak(f"Sorry, I couldn't find the stock data for {ticker.upper()}.")
                else:
                    text_to_speech.speak("Sorry, I couldn't resolve the stock ticker from your input.")
            
            elif "exit" in user_input or "quit" in user_input:
                text_to_speech.speak("Goodbye! Have a great day!")
                break  # Exit the loop and end the conversation
                
            else:
                text_to_speech.speak("Sorry, I didn't understand that. Could you repeat?")
        
        time.sleep(1)  # Short pause before next recognition

if __name__ == "__main__":
    start_conversation()

