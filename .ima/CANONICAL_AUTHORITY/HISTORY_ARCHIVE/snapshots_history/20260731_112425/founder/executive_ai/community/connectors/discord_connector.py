from .base_connector import BaseConnector


class DiscordConnector(BaseConnector):

    name="discord"

    def fetch(self):

        return []

    def receive_event(self,event):

        return {
            "source":"discord",
            "type":"community_signal",
            "content":event
        }
