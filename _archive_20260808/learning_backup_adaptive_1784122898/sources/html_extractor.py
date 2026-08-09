import re
from html import unescape

def extract_text(html):

    if not html:
        return ""

    html = re.sub(
        r"<script.*?</script>",
        "",
        html,
        flags=re.S
    )

    html = re.sub(
        r"<style.*?</style>",
        "",
        html,
        flags=re.S
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        html
    )

    text = unescape(text)

    text = " ".join(text.split())

    return text[:5000]
