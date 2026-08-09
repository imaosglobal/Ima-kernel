class BaseConnector:

    name="base"

    def fetch(self):

        return []

    def normalize(self,item):

        return {
            "source":self.name,
            "content":item
        }
