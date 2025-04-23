from dotenv import load_dotenv
import os
import openai
load_dotenv()  # This loads variables from .env into the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"

def call_groq(prompt, model="mixtral-8x7b-32768", max_tokens=100):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"[GROQ ERROR]: {e}")
        return None
