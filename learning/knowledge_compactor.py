
import hashlib


    return hashlib.sha256(
        text.encode("utf8")
    ).hexdigest()


def compact(text):

    if not text:
        return ""

    text=" ".join(
        text.split()
    )

    return text[:3000]
