def detect_inflation(text):
    """
    Simulated inflation detection.
    Real logic would involve NLP to detect subjective claims vs objective facts.
    """
    # Placeholder: Just keyword matching for "expert in everything" or too many buzzwords
    suspicious_phrases = ["expert in all", "100% success", "world class"]
    
    flags = []
    text_lower = text.lower()
    for phrase in suspicious_phrases:
        if phrase in text_lower:
            flags.append(f"Suspicious claim found: '{phrase}'")
            
    return flags
