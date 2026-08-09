class InputBuffer:
    def __init__(self):
        self.active = False
        self.buffer = []

    def add(self, text):
        if not text:
            return None

        text = str(text).strip()

        # הודעה רגילה
        if not self.active:
            if text == "FILE" or text.startswith("FILE\n") or text.startswith("קבלי קובץ"):
                self.active = True
                self.buffer = [text]
                return None

            return text

        # איסוף קובץ
        if text == "END":
            content = "\n".join(self.buffer)
            self.reset()
            return content

        self.buffer.append(text)
        return None

    def reset(self):
        self.active = False
        self.buffer = []
