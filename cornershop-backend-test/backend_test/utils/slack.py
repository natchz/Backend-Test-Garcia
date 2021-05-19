import os
from slack_sdk import WebClient
from backend_test.utils.singleton import SingletonMeta
from backend_test.envtools import getenv

class SlackClient(metaclass=SingletonMeta):
    """
    Slack client with singleton implementation, it will only take time
    with the first call
    """

    def __init__(self):
        # The token will be necessary to authenticate the requests
        self.client = WebClient(token=getenv("SLACK_BOT_TOKEN"))

    def send_user_message(self, user, text):
        """
        Send a private message to the user with the reported id
        """
        return self.client.chat_postMessage(
            channel=user,
            text=text,
        )