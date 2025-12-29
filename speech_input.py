import vosk
import pyaudio
import json
import time

# Load Vosk model (download beforehand)
model = vosk.Model("vosk-model-small-en-in-0.4")
recognizer = vosk.KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = None

# Words to ignore (robot's own speech fragments)
IGNORE_WORDS = [
    "school", "reception", "system", "online", "anything",
    "welcome", "great", "day", "help", "you",
    "timings", "from", "principal", "office", "first", "floor",
    "admissions", "please", "visit", "near", "entrance",
    "located", "second", "available", "staircase",
    "straight", "ahead", "sorry", "understand", "again"
]

def init_stream():
    """Initialize the audio stream"""
    global stream
    if stream is None:
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        stream.start_stream()
    return stream

def close_stream():
    """Completely close the audio stream"""
    global stream
    if stream is not None:
        try:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        except:
            pass
        stream = None

def pause_stream():
    """Pause the audio stream before speaking"""
    close_stream()  # Completely close instead of just pausing

def resume_stream():
    """Resume the audio stream after speaking"""
    global stream
    if stream is None:
        init_stream()
    elif not stream.is_active():
        stream.start_stream()

def clear_buffer():
    """Clear the audio buffer and recognizer state"""
    global stream, recognizer
    # Reset the recognizer to clear any partial results
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    # Read and discard any buffered audio
    if stream is not None and stream.is_active():
        try:
            for _ in range(10):  # Clear more buffer
                stream.read(8192, exception_on_overflow=False)
        except:
            pass

def is_valid_input(text):
    """Check if the text is valid user input (not robot's own voice)"""
    if not text:
        return False
    
    words = text.split()
    
    # If ALL words are in ignore list, it's probably robot's voice
    meaningful_words = [w for w in words if w not in IGNORE_WORDS]
    
    # Need at least one meaningful word
    return len(meaningful_words) > 0

def listen(timeout=10):
    """
    Listens from microphone and returns recognized text.
    Returns empty string if timeout is reached or no speech detected.
    """
    global stream, recognizer
    
    # Reinitialize stream and recognizer fresh
    close_stream()
    time.sleep(0.2)  # Small delay
    recognizer = vosk.KaldiRecognizer(model, 16000)
    init_stream()
    clear_buffer()
    
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            return ""
        
        try:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                
                # Only return if it's valid user input
                if text and is_valid_input(text):
                    return text
        except Exception as e:
            print(f"Audio read error: {e}")
            return ""
        except Exception as e:
            print(f"Audio read error: {e}")
            return ""
