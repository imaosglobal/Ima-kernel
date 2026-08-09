SUPPORTED_LANGUAGES=[
"he",
"en",
"ar",
"es",
"fr",
"de",
"zh",
"ja",
"ru",
"hi"
]


def detect_language(text):

    return "auto_detected"


def translate(text,target):

    return {
        "original":text,
        "target":target,
        "translation_ready":True
    }
