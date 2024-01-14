import asyncio
import os
from streamingbot import create_streamingbot


TWITCH_USERS = os.environ.get('TWITCH_USERS')
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')


async def main():
    bot = await create_streamingbot(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, SLACK_WEBHOOK_URL)
    bot.add_users_to_watch([u.strip() for u in TWITCH_USERS.split(",")])
    await bot.run()


def lambda_handler(event, context):  #pylint: disable=unused-argument
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
