import os
import json
from groq import Groq

# Initialize Groq client using env var
client = Groq(api_key="gsk_1Esg25RTURm6158QnvpqWGdyb3FY4xNBvDne1D6eIoAvdbbdxBvJ2g3a1e4")

def process_with_groq(user_input):
    """
    Send user input to Groq and return structured intent, ticker, and response.
    """
    try:
        prompt = f"""
        You are a stock market assistant. Analyze this input and respond with a JSON object with these keys:
        - intent: either 'stock_price', 'exit', 'greeting', or 'general'
        - ticker: valid stock ticker symbol (if applicable, else null)
        - response: what you would say in response to the user

        Input: "{user_input}"
        """

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # You can sub in other Groq-supported models
            messages=[
                {"role": "system", "content": "You are a helpful assistant that replies in JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        parsed_response = json.loads(response.choices[0].message.content)
        return parsed_response

    except Exception as e:
        print(f"[Groq Error] {e}")
        return {
            "intent": "general",
            "ticker": None,
            "response": "Sorry, I ran into an issue trying to process that. Could you say it again?"
        }
def groq_ticker_resolution(user_input):
    """
    Use Groq to resolve stock ticker from user input.
    Returns the ticker symbol if found, else None.
    """
    result = process_with_groq(user_input)
    if result["intent"] == "stock_price" and result["ticker"]:
        return result["ticker"]
    return None
def extract_intent_from_groq(user_input):
    """
    Extract intent from the Groq response.
    Uses Groq's response structure to identify the intent.
    """
    result = process_with_groq(user_input)
    # Assuming Groq response has an 'intent' field, adapt if needed
    if "intent" in result:
        return result["intent"]
    return None
def extract_response_from_groq(user_input):
    """
    Extract response from the Groq response.
    Uses Groq's response structure to identify the response.
    """
    result = process_with_groq(user_input)
    # Assuming Groq response has a 'response' field, adapt if needed
    if "response" in result:
        return result["response"]
    return None

def extract_ticker_from_groq(user_input):
    """
    Extract stock ticker from the Groq response.
    Uses Groq's response structure to identify the stock ticker.
    """
    result = process_with_groq(user_input)
    # Assuming Groq response has a 'ticker' field, adapt if needed
    if "ticker" in result:
        return result["ticker"]
    return None
