from languages.language_engine import detect_language, language_info
from founder.executive_ai.device.device_language import detect_device_language
from founder.executive_ai.global_intelligence.world_people_index import COUNTRIES


def get_language_context(message, person=None):

    message_language = detect_language(message)

    device_language = detect_device_language()

    country = "unknown"

    if person:
        country = person.get(
            "country",
            "unknown"
        )

    country_info = COUNTRIES.get(
        country,
        {}
    )

    return {
        "message_language": message_language,

        "device_language": device_language,

        "language_profile":
            language_info(message_language)
            if message_language != "unknown"
            else None,

        "country": country,

        "country_languages":
            country_info.get(
                "languages",
                []
            )
    }
