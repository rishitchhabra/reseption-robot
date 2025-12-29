from speech_input import listen, init_stream
from speech_output import speak
from intents import get_response
from wakeword import is_wake_word
import time

def main():
    """Main function to run the school reception system"""
    # Initialize the audio stream
    init_stream()
    
    speak("School reception system is online. You can ask me anything.")
    
    while True:
        try:
            print("\nListening...")
            text = listen(timeout=15)
    
            if not text:
                continue
    
            print("Heard:", text)
    
            # Check if it's a wake word (greeting)
            if is_wake_word(text):
                speak("Hello! How can I help you?")
                continue
            
            # Check if user said goodbye
            if any(word in text for word in ["bye", "goodbye", "thank", "thanks"]):
                speak("You're welcome! Have a great day!")
                continue
            
            # Otherwise, treat it as a question and respond
            response = get_response(text)
            speak(response)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
