import json
from pathlib import Path

CONCEPT_FILE = Path("languages/concepts/concept_translation.json")


def translate_concepts(text, language):
    try:
        data = json.loads(
            CONCEPT_FILE.read_text(encoding="utf-8")
        )

        for concept, langs in data.items():
            if language in langs:
                text = text.replace(
                    concept,
                    langs[language]
                )

    except Exception:
        pass

    return text


def translate_response(text, language):

    translations = {
        "en": {
            "אני IMA.": "I am IMA.",
            "אני כאן כדי להקשיב, להבין ולעזור לך דרך השיחה שלנו.": 
            "I am here to listen, understand and help you through our conversation.",
            "אני זוכרת שדיברנו גם על:": 
            "I remember we also talked about:"
        },

        "ar": {
            "אני IMA.": "أنا IMA.",
            "אני כאן כדי להקשיב, להבין ולעזור לך דרך השיחה שלנו.": 
            "أنا هنا للاستماع والفهم والمساعدة من خلال حديثنا.",
            "אני זוכרת שדיברנו גם על:":
            "I remember we also talked about:": "أتذكر أننا تحدثنا أيضًا عن:"
        },

        "es": {
            "אני IMA.": "Soy IMA.",
            "אני זוכרת שדיברנו גם על:":
            "Recuerdo que también hablamos de:"
        },

        "fr": {
            "אני IMA.": "Je suis IMA.",
            "אני זוכרת שדיברנו גם על:":
            "Je me souviens que nous avons aussi parlé de:"
        }
    }

    if language not in translations:
        return text

    result = text

    for source, target in translations[language].items():
        result = result.replace(source, target)

    result = translate_concepts(result, language)

    return result
