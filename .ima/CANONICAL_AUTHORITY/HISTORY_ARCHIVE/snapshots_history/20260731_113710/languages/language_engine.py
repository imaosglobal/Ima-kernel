from pathlib import Path
import json

PROFILE_FILE = Path("languages/language_profiles.json")


def load_languages():
    return json.loads(
        PROFILE_FILE.read_text(encoding="utf-8")
    )


def detect_language(text):

    if any('\u0590' <= c <= '\u05FF' for c in text):
        return "he"

    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    if any(word in text.lower().split() for word in [
        "hello", "what", "why", "how"
    ]):
        return "en"

    if any(word in text.lower() for word in [
        "hola", "gracias"
    ]):
        return "es"

    if any(word in text.lower() for word in [
        "bonjour", "merci"
    ]):
        return "fr"

    return "unknown"


def language_info(code):
    return load_languages().get(code)
