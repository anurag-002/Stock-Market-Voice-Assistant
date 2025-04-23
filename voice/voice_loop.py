import time
import speech_to_text
import text_to_speech

def start_conversation():
    print("Voice assistant activated. How can I help you today?")
    
    while True:
        # Step 1: Capture speech
        user_input = speech_to_text.convert_speech_to_text()  # Capture voice input
        
        if user_input.lower() == "stop":
            print("Shutting down the assistant...")
            break
        
        # Step 2: Generate a response (simple echo for now, can be replaced by your logic)
        print(f"You said: {user_input}")
        response = f"You said: {user_input}"  # Placeholder response logic
        
        # Step 3: Convert the response into speech
        text_to_speech.convert_text_to_speech(response)  # Speak the response
        
        # Step 4: Wait for a short time before accepting the next input (to allow for proper pauses)
        time.sleep(3)  # Adjust this as necessary for your needs

if __name__ == "__main__":
    start_conversation()
