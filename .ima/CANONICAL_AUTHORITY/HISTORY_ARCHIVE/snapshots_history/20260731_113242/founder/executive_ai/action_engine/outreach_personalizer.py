from founder.executive_ai.global_intelligence.language_preference import choose_outreach_language


def personalize_outreach(profile, purpose="IMA collaboration"):

    language = choose_outreach_language(profile)

    name = profile.get(
        "name",
        "friend"
    )

    templates = {
        "he": f"שלום {name}, IMA מזהה אפשרות לשיתוף פעולה בתחום {purpose}.",
        "en": f"Hello {name}, IMA identified a possible collaboration opportunity in {purpose}.",
        "ja": f"こんにちは {name}さん、IMAは{purpose}で協力の可能性を見つけました。",
        "ar": f"مرحبا {name}، حددت IMA إمكانية للتعاون في مجال {purpose}."
    }

    return {
        "language": language,
        "message": templates.get(
            language,
            templates["en"]
        )
    }
