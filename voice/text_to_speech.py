from gtts import gTTS
import os
import time

def text_to_speech_live(text, lang='en', slow=False):
    """
    Converts the provided text to speech and plays it live for a voice assistant.
    
    Parameters:
    - text (str): The text to convert to speech.
    - lang (str): Language of the speech (default is 'en' for English).
    - slow (bool): Whether the speech should be slow (default is False).
    """
    try:
        # Convert the text to speech
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save the speech to a file temporarily
        tts.save("temp_audio.mp3")
        
        # Play the audio (system dependent)
        os.system("start temp_audio.mp3")  # For Windows
        # On Linux or MacOS, use: os.system("mpg321 temp_audio.mp3") or os.system("afplay temp_audio.mp3")
        
        # Sleep for 3 seconds after the speech finishes
        time.sleep(3)  # Adjust this value as needed to wait for 3 seconds after speaking

    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
