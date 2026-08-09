class ChatConnector:

    def __init__(self,name):
        self.name=name


    def handle(self,user,message):

        return {
            "platform":self.name,
            "user":user,
            "message":message,
            "status":"received",
            "next":"IMA_processing"
        }
