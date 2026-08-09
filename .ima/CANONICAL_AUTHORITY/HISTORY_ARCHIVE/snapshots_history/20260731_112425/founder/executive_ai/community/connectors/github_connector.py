from .base_connector import BaseConnector


class GithubConnector(BaseConnector):

    name="github"

    def fetch(self):

        return []

    def receive_webhook(self,event):

        return {
            "source":"github",
            "type":"contribution",
            "content":event
        }
