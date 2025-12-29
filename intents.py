INTENTS = {
    "timing": "School timings are from 8 AM to 2 PM.",
    "time": "School timings are from 8 AM to 2 PM.",
    "principal": "The principal's office is on the first floor.",
    "admission": "For admissions, please visit the office near the entrance.",
    "library": "The library is located on the second floor.",
    "washroom": "Washrooms are available near the staircase.",
    "bathroom": "Washrooms are available near the staircase.",
    "toilet": "Washrooms are available near the staircase.",
    "exit": "The exit gate is straight ahead.",
    "gate": "The exit gate is straight ahead.",
    "help": "I can help you with school timings, principal office location, admissions, library, washrooms, and exit."
}

def get_response(text):
    """
    Matches user input with predefined intents
    """
    if not text:
        return "Sorry, I did not hear anything. Please try again."
    
    text = text.lower().strip()
    
    for keyword in INTENTS:
        if keyword in text:
            return INTENTS[keyword]
    return "Sorry, I did not understand that. Please ask again."
