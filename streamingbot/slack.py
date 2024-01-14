"""
Slack message handler
"""
import json
import arrow
import requests
from requests.models import Response
from twitchAPI.twitch import Stream, TwitchUser


class SlackHandler:
    """ Slack message handler """
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.session = requests.Session()

    @staticmethod
    def _gen_thumbnail_url(url: str, width: int, height: int) -> str:
        """ Generate thumbnail URL with desired resolution """
        return url.replace("{width}", str(width)).replace("{height}", str(height))

    def send_message(self, stream: Stream, user: TwitchUser) -> Response:
        """ Post to Slack """
        headers = {'Content-Type': 'application/json'}

        time_ago = arrow.get(stream.started_at).humanize()

        title = f"*{stream.user_login}* started a live stream {time_ago}!"
        text = (
            f"*<https://twitch.tv/{stream.user_login}|{stream.user_name} - Twitch>*\n"
            f"{stream.title}"
        )

        msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": title
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "image",
                    "image_url": self._gen_thumbnail_url(stream.thumbnail_url, 640, 360),
                    "alt_text": stream.title
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": user.profile_image_url,
                        "alt_text": stream.user_login
                    }
                },
                {
                    "type": "divider"
                }
            ]
        }

        return self.session.post(
            self.webhook_url,
            headers=headers,
            data=json.dumps(msg)
        )
