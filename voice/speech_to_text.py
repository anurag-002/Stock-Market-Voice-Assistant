# speech_to_text.py

import speech_recognition as sr

def convert_speech_to_text():
    recognizer = sr.Recognizer()
    
    # Use the default microphone
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection")
        return None
