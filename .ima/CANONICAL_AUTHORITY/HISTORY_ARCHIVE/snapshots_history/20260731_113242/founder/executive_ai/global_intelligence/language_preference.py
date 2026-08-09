def choose_outreach_language(profile):

    detected = profile.get(
        "detected_language"
    )

    languages = profile.get(
        "languages",
        []
    )


    mapping={
        "Hebrew":"he",
        "Arabic":"ar",
        "English":"en",
        "Japanese":"ja",
        "Spanish":"es",
        "French":"fr",
        "German":"de",
        "Chinese":"zh",
        "Russian":"ru"
    }


    # שפת הודעת המשתמש
    if detected and detected != "unknown":
        return detected


    # שפת המדינה / האדם
    for lang in languages:
        if lang in mapping:
            return mapping[lang]


    # fallback
    return "en"
