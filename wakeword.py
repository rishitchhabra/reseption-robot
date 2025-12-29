# Individual greeting words to detect
GREETING_WORDS = ["hello", "hi", "hey", "hola", "namaste"]

def is_wake_word(text):
    """
    Checks if any greeting word is present in the text
    """
    if not text:
        return False
    words = text.lower().split()
    return any(greet in words for greet in GREETING_WORDS)
