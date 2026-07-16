from learning.sources.html_extractor import clean_html


def clean_source(item):
    if not item:
        return None

    text=item.get("content","")

    if not text:
        return None

    if "<html" in text.lower() or "<!doctype" in text.lower():
        text=clean_html(text)

    item["content"]=text[:5000]

    if len(text)<50:
        return None

    return item
