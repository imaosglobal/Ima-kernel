from founder.executive_ai.language.language_context_bridge import get_language_context


def build_human_profile(person, message=""):

    language_context = get_language_context(
        message,
        person
    )

    language_profile = language_context.get(
        "language_profile"
    ) or {}

    return {
        "name": person.get(
            "name",
            "unknown"
        ),

        "country": person.get(
            "country",
            "unknown"
        ),

        "languages": language_context.get(
            "country_languages",
            []
        ),

        "message_language": language_context.get(
            "message_language"
        ),

        "device_language": language_context.get(
            "device_language"
        ),

        "communication": {
            "direction": language_profile.get(
                "direction",
                "ltr"
            )
        }
    }
