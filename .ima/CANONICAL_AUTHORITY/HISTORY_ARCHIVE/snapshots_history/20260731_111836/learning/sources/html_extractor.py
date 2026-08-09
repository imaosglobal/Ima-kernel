import re
from html import unescape

def extract_text(html):
    if not html:
        return ""

    html=re.sub(
        r"<(script|style|head|noscript).*?>.*?</\\1>",
        "",
        html,
        flags=re.I|re.S
    )

    html=re.sub(
        r"<[^>]+>",
        " ",
        html
    )

    text=unescape(html)

    # ניקוי CSS ו-JS שנשארו
    text=re.sub(
        r"\\b(var|function|document|window|gform)\\b[^ ]*",
        "",
        text,
        flags=re.I
    )

    text=re.sub(
        r"[^\\w\\s.,!?א-ת]",
        " ",
        text
    )

    text=" ".join(text.split())

    return text[:5000]
