import os
import locale


def detect_device_language():

    candidates=[]

    # Android / Linux locale
    for key in [
        "LANG",
        "LANGUAGE",
        "LC_ALL"
    ]:
        value=os.environ.get(key)
        if value:
            candidates.append(value)

    try:
        loc=locale.getdefaultlocale()[0]
        if loc:
            candidates.append(loc)
    except:
        pass


    for item in candidates:

        item=item.lower()

        if item.startswith("he"):
            return "he"

        if item.startswith("ar"):
            return "ar"

        if item.startswith("en"):
            return "en"

        if item.startswith("es"):
            return "es"

        if item.startswith("fr"):
            return "fr"

        if item.startswith("ru"):
            return "ru"

        if item.startswith("de"):
            return "de"

        if item.startswith("zh"):
            return "zh"

        if item.startswith("ja"):
            return "ja"


    return "en"
