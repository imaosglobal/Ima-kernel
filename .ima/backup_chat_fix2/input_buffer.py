
class InputBuffer:
    def __init__(self):
        self.active=False
        self.buffer=[]

    def add(self,text):
        if not text:
            return None

        text=str(text)

        if not self.active:
            if text.strip() in ["FILE","```","קבלי קובץ"]:
                self.active=True
                self.buffer=[]
                return None
            return text

        if text.strip() in ["END","```"]:
            data="\n".join(self.buffer)
            self.reset()
            return data

        self.buffer.append(text)
        return None

    def reset(self):
        self.active=False
        self.buffer=[]
