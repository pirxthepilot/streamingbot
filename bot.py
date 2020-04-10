import os
import json

import arrow
import requests
import twitch


TWITCH_USER = os.environ.get('TWITCH_USER')
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

tw = twitch.Helix(TWITCH_CLIENT_ID)

# Get followings
#followings = tw.user(TWITCH_USER).following().users
#
#for user in followings:
#    print(user)
#    #if user.is_live:
#    #    print(f"{user} stream: {user.stream}")


user = tw.user(TWITCH_USER)
stream = user.stream
print(stream.id)
print(stream.user_id)
print(user.id)

slack = requests.Session()
headers = {'Content-Type': 'application/json'}

time_ago = arrow.get(stream.started_at).humanize()
title = f"*{user.login}* started a live stream {time_ago}!"
text = (
    f"*<https://twitch.tv/{user.login}|{user.display_name} - Twitch>*\n"
    f"{stream.title}"
)
stream_thumbnail_url = stream.thumbnail_url.format(width=800, height=450)

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

resp = slack.post(SLACK_WEBHOOK_URL, headers=headers, data=json.dumps(msg))
print(resp.status_code)
print(resp.text)
