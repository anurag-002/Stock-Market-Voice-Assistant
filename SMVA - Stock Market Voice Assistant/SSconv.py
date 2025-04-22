import speech_recognition as sr
from gtts import gTTS
from groq import Groq
import os
import tempfile
import time
import random
import pygame
import yfinance as yf   # For stock data fetching       

# 🔐 Your Groq API Key
client = Groq(api_key="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")

recognizer = sr.Recognizer()

# 🎵 Initialize pygame for audio playback
pygame.mixer.init()

class SSconv:
    @staticmethod
    def Output(text):
        """Speak text with expressive Gen Z-style and play it using pygame."""
        print(f"\n🤖 Assistant (speaking): {text}")

        intro_phrases = ["yo,", "uhh,", "bro,", "hmm,", "okay,", "sheesh,", "dang,"]
        hype_phrases = ["let's gooo!", "you nailed it!", "ayy that's lit!", "boom!", "oh snap!"]

        if any(word in text.lower() for word in ["error", "failed", "sorry", "can't"]):
            text = f"{random.choice(['ah damn,', 'ugh,', 'bro...'])} {text}"
        elif any(word in text.lower() for word in ["congrats", "awesome", "level up", "!"]):
            text = f"{random.choice(hype_phrases)} {text}"
        else:
            if random.random() < 0.3:
                text = f"{random.choice(intro_phrases)} {text}"

        try:
            tts = gTTS(text=text, lang="en", slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            temp_path = temp_file.name
            temp_file.close()

            for _ in range(3):
                try:
                    time.sleep(0.2)
                    pygame.mixer.music.load(temp_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    break
                except PermissionError as e:
                    print(f"⚠️ Retry due to file lock: {e}")
                    time.sleep(0.3)
                except Exception as e:
                    print(f"❌ Failed playing audio: {e}")
                    break

            os.unlink(temp_path)
            return True
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            return False

    @staticmethod
    def Input(timeout=5, phrase_time_limit=10):
        """Capture and return user's voice input as text. Falls back to typed input if mic fails."""
        print("\n🎤 Listening for your voice... (Speak now)")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("🧠 Processing what you said...")
                text = recognizer.recognize_google(audio)
                print(f"\n🗣️ You said: {text}")
                return text.lower()
        except Exception as e:
            print(f"⚠️ Mic failed: {e}")
            fallback = input("⌨️ Mic broke—type instead: ")
            return fallback.lower() if fallback.strip() else None

    @staticmethod
    def GroqReply(prompt):
        """Get a smart, witty response from the Groq LLaMA 3 model, optionally enhanced with stock data."""
        keywords = ["stock", "price", "market", "ticker", "share", "invest", "value"]
        tickers = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NVDA", "NFLX", "META", "BABA", "AMD"]

        matched_ticker = None
        for ticker in tickers:
            if ticker.lower() in prompt.lower():
                matched_ticker = ticker
                break

        stock_info = ""
        if any(word in prompt.lower() for word in keywords) and matched_ticker:
            try:
                stock = yf.Ticker(matched_ticker)
                data = stock.history(period="1d", interval="1m").tail(1)
                if not data.empty:
                    latest = data.iloc[-1]
                    price = latest['Close']
                    time_stamp = latest.name.strftime('%Y-%m-%d %H:%M:%S')
                    stock_info = f"\nFYI: As of {time_stamp}, {matched_ticker} is trading at ${price:.2f}."
                else:
                    stock_info = f"\nCouldn't fetch current price for {matched_ticker}. Might be after hours."
            except Exception:
                stock_info = f"\nHad trouble fetching data for {matched_ticker}."

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You're a helpful, witty AI that talks like a 22-year-old friend. Keep it chill and expressive."},
                    {"role": "user", "content": prompt + stock_info}
                ],
                temperature=0.9,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error getting Groq response: {e}")
            return "Yo, my brain just glitched. Can we try again?"

# 🚀 Standalone interaction loop (runs only when file is executed directly)
def main():
    SSconv.Output("Yo! I'm your AI homie. What do you wanna talk about?")

    while True:
        command = SSconv.Input()
        if command:
            if command in ["exit", "quit", "bye"]:
                SSconv.Output("Peace out!")
                print("👋 Exiting...")
                break

            reply = SSconv.GroqReply(command)
            SSconv.Output(reply)

if __name__ == "__main__":
    main()