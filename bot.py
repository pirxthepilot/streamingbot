import os
from streamingbot import StreamingBot


TWITCH_USER = os.environ.get('TWITCH_USER')
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')


def main():
    bot = StreamingBot(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, SLACK_WEBHOOK_URL)
    bot.set_users_to_watch(bot.get_user_follows(TWITCH_USER))
    bot.run()


def lambda_handler(event, context):  #pylint: disable=unused-argument
    main()


if __name__ == '__main__':
    main()
