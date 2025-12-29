import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speech speed

voices = engine.getProperty('voices')

for v in voices:
    if "Veena" in v.name:   # change name if needed
        engine.setProperty('voice', v.id)
        break


# Store references to avoid circular import issues
_close_stream = None
_clear_buffer = None

def _get_stream_functions():
    """Lazy load stream functions to avoid circular imports"""
    global _close_stream, _clear_buffer
    if _close_stream is None:
        try:
            from speech_input import close_stream, clear_buffer
            _close_stream = close_stream
            _clear_buffer = clear_buffer
        except ImportError:
            _close_stream = lambda: None
            _clear_buffer = lambda: None
    return _close_stream, _clear_buffer

def speak(text):
    """
    Converts text to speech
    """
    close_fn, clear_fn = _get_stream_functions()
    
    # Completely close microphone before speaking
    try:
        close_fn()
    except Exception:
        pass
    
    # Wait for mic to fully close
    time.sleep(0.2)
    
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")
    
    # Wait for audio to completely settle (longer delay)
    time.sleep(1.0)

