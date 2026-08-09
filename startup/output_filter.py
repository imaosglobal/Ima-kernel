class OutputFilter:

    REMOVE = [
        "מנגן קול... 🔊",
    ]

    def clean(self, text):
        if not isinstance(text, str):
            return text

        for item in self.REMOVE:
            text = text.replace(item, "")

        return text.strip()
