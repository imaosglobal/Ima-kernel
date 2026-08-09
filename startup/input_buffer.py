class InputBuffer:
    def __init__(self):
        self.active=False
        self.buffer=[]

    def add(self,text):
        text=str(text)

        if not self.active:
            if text.strip() in ["FILE","```"]:
                self.active=True
                self.buffer=[]
                return None

            return text

        if text.strip()=="END" or text.strip()=="```":
            data="\n".join(self.buffer)
            self.reset()
            return data

        self.buffer.append(text)
        return None

    def reset(self):
        self.active=False
        self.buffer=[]
