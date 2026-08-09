def analyze_patterns(data=None):

    data=data or []

    return {
        "patterns_found": len(data),
        "patterns": data[-10:]
    }
