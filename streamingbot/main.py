"""
Main routine
"""
from typing import AsyncGenerator, Dict, List

from botocore.exceptions import ClientError
from twitchAPI.twitch import Stream, Twitch, TwitchUser

from streamingbot.db import DynamoDBHandler
from streamingbot.slack import SlackHandler


DB_NAME = 'streamingbotdb'


class StreamingBot:
    """ Streamingbot yay! """
    def __init__(self,
        slack_webhook_url: str
    ) -> None:
        self.sl = SlackHandler(slack_webhook_url)  # Slack session
        self.db = DynamoDBHandler(DB_NAME)         # DynamoDB session
        self.users: List[str] = []                 # Twitch users to monitor for status
        self.streams: Dict[str, Stream] = {}       # Current streams
        self.saved: Dict[str, dict] = {}           # Saved items in the DB

    async def _init_twitch_client(self, twitch_client_id, twitch_client_secret):
        self.tw = await Twitch(twitch_client_id, twitch_client_secret)

    async def get_streams(self) -> AsyncGenerator[Stream, None]:
        """ Get current live streams """
        async for stream in self.tw.get_streams(user_login=self.users, first=100):
            yield stream

    async def get_users(self, users: List[str]) -> AsyncGenerator[TwitchUser, None]:
        """ Get user detail """
        async for user in self.tw.get_users(logins=users):
            yield user

    def add_users_to_watch(self, users: List[str]) -> None:
        """ Add to self.users """
        self.users += users

    async def run(self):
        """ Main routine """
        if not self.users:
            print('No users in my list! Exiting.')
            return

        print(f"{len(self.users)} users in my list")

        # Get a snapshot of items in DB before we begin
        self._get_db_snapshot()

        # Begin!
        async for stream in self.get_streams():
            self.streams[stream.id] = stream
            print(f"[{stream.user_login}] is live!")

            # Process the stream
            try:
                # First check if stream is already in DB
                if stream.id in self.saved:
                    print(
                        f"I am already aware of {stream.user_login}'s stream "
                        f"(ID: {stream.id}) - skipping Slack messaging"
                    )
                    continue

                # Save to DB
                print(f"{stream.user_login}'s stream (ID: {stream.id}) is new!")
                self._save_to_db(stream)
                print(f"Stream {stream.id} saved to DB")

            except ClientError as e:
                print(f"DYNAMODB ERROR: {e}")
                continue

        # Send to Slack

        # First get user data in bulk for info not found in stream (e.g. profile image URL)
        streams_to_process = [s for s in self.streams.values() if s.id not in self.saved]
        user_data: Dict[str, TwitchUser] = {}
        if streams_to_process:
            async for user in self.get_users([s.user_login for s in streams_to_process]):
                user_data[user.login] = user

        # Now send the messages
        for stream in streams_to_process:
            resp = self.sl.send_message(stream, user_data[stream.user_login])
            print(
                f"Sent message to Slack for {stream.user_login} with result: "
                f"{resp.status_code} {resp.text}"
            )

        # DB cleanup
        print('Cleaning up DB items where applicable...')
        for stream_id, stream in self.saved.items():
            if stream_id not in self.streams:
                print(f"{stream['user_login']} no longer streams "
                      f"{stream_id}")
                try:
                    self._remove_from_db(stream_id)
                    print(f"Stream {stream_id} removed from DB")
                except ClientError as e:
                    print(f"DynamoDB error removing from DB: {e}")
                    continue
        print('All done!')

    def _get_db_snapshot(self) -> None:
        """ Load DB content into self.saved """
        for row in self.db.scan():
            self.saved[row["stream_id"]] = row

    def _save_to_db(self, stream: Stream) -> None:
        """ Save stream to DB """
        self.db.put_item(**{
            'stream_id': stream.id,
            'user_login': stream.user_login,
            'started_at': str(stream.started_at),
        })

    def _remove_from_db(self, stream_id: str) -> None:
        """ Remove stream from DB """
        self.db.delete_item("stream_id", stream_id)


async def create_streamingbot(
        twitch_client_id: str,
        twitch_client_secret: str,
        slack_webhook_url: str
) -> StreamingBot:
    """ Create the Streamingbot instance """
    sb = StreamingBot(slack_webhook_url)
    await sb._init_twitch_client(twitch_client_id, twitch_client_secret)
    return sb
