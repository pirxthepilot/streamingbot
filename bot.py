import os
from streamingbot import StreamingBot


TWITCH_USER = os.environ.get('TWITCH_USER')
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')


def main():
    bot = StreamingBot(TWITCH_CLIENT_ID, SLACK_WEBHOOK_URL)
    bot.set_users_to_watch(bot.get_user_follows(TWITCH_USER))
    bot.run()


def lambda_handler():
    main()


if __name__ == '__main__':
    main()
