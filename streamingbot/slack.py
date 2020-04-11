import json
import arrow
import requests
from requests.models import Response
from twitch.helix.models.user import User
from twitch.helix.models.stream import Stream


class SlackHandler:
    """ Slack message handler """
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.session = requests.Session()

    def send_message(self, user: User, stream: Stream) -> Response:
        """ Post to Slack """
        headers = {'Content-Type': 'application/json'}

        time_ago = arrow.get(stream.started_at).humanize()

        title = f"*{user.login}* started a live stream {time_ago}!"
        text = (
            f"*<https://twitch.tv/{user.login}|{user.display_name} - Twitch>*\n"
            f"{stream.title}"
        )
        # stream_thumbnail_url = stream.thumbnail_url.format(width=800, height=450)

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
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": user.profile_image_url,
                        "alt_text": user.login
                    }
                },
                # {
                #     "type": "divider"
                # },
                # {
                #     "type": "image",
                #     "title": {
                #         "type": "plain_text",
                #         "text": "Screenshot",
                #         "emoji": True
                #     },
                #     "image_url": stream_thumbnail_url,
                #     "alt_text": stream.title
                # },
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

