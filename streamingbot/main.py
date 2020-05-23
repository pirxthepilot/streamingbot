from typing import List, Optional

from botocore.exceptions import ClientError

import requests
import twitch
from twitch.helix.models.user import User
from twitch.helix.models.stream import Stream
from twitch.helix import StreamNotFound

from streamingbot.db import DynamoDBHandler
from streamingbot.exceptions import StreamingBotException
from streamingbot.slack import SlackHandler


DB_NAME = 'streamingbotdb'


class StreamingBot:
    """ Streamingbot yay! """
    TWITCH_AUTH_BASEURL = 'https://id.twitch.tv'

    def __init__(self,
        twitch_client_id: str,
        twitch_client_secret: str,
        slack_webhook_url: str
    ) -> None:
        self.tw = twitch.Helix(                    # Twitch session
            twitch_client_id,
            twitch_client_secret,
            bearer_token=self._get_token(
                twitch_client_id,
                twitch_client_secret,
            )
        )
        self.sl = SlackHandler(slack_webhook_url)  # Slack session
        self.db = DynamoDBHandler(DB_NAME)         # DynamoDB session
        self.users: List[User] = []                # Twitch users to watch
        self.streams: List[Stream] = []            # List of current streams
        self.saved: List[dict] = []                # Saved items in the DB

    @staticmethod
    def _get_token(client_id, client_secret) -> str:
        """ Get the app access OAuth token """
        try:
            resp = requests.post(
                f"{StreamingBot.TWITCH_AUTH_BASEURL}/oauth2/token",
                params={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'grant_type': 'client_credentials',
                }
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
             raise StreamingBotException(f"Error getting token: {e}")

        return resp.json().get('access_token')

    def set_users_to_watch(self, users: List[User]) -> None:
        """ Populate self.users """
        self.users = users

    def get_users(self, user_logins: List[str]) -> Optional[List[User]]:
        """ Get a list of User instances based on login name """
        users = []
        for login in user_logins:
            user = self.tw.user(login)
            if user is not None:
                users.append(user)
        return users

    def get_user_follows(self, user_login: str) -> Optional[List[User]]:
        """ Given a login name, return a list of users it follows """
        users = []
        for user in self.tw.user(user_login).following().users:
            users.append(user)
        return users

    def run(self):
        """ Main routine """
        if not self.users:
            print('No users in my list! Exiting.')
            return

        print(f"{len(self.users)} users in my list")

        # Get a snapshot of items in DB before we begin
        self.saved = self.db.scan()

        # Begin!
        for user in self.users:
            try:
                stream = user.stream
                self.streams.append(stream)
                print(f"[{user.login}] is live!")
            except StreamNotFound:
                print(f"[{user.login}] is not streaming")
                continue

            # Process the streamer
            try:
                # First check if stream is already in DB
                if self._exists_in_db(stream.id):
                    print(
                        f"I am already aware of {user.login}'s stream "
                        f"(ID: {stream.id}) - skipping Slack messaging"
                    )
                    continue

                # Save to DB
                print(f"{user.login}'s stream (ID: {stream.id}) is new!")
                self._save_to_db(user, stream)
                print(f"Stream {stream.id} saved to DB")

                # Send to Slack
                resp = self.sl.send_message(user, stream)
                print(
                    f"Sent message to Slack for {user.login} with result: "
                    f"{resp.status_code} {resp.text}"
                )
            except ClientError as e:
                print(f"DYNAMODB ERROR: {e}")
                continue

        # DB cleanup (TBD)
        print('Cleaning up DB items where applicable...')
        for stream in self.saved:
            #print(f"Is {stream['stream_id']} in {[i.id for i in self.streams]}")
            if not self._exists_in_streams(stream['stream_id']):
                print(f"{stream['user_login']} no longer streams "
                      f"{stream['stream_id']}")
                try:
                    self._remove_from_db(stream['stream_id'])
                    print(f"Stream {stream['stream_id']} removed from DB")
                except ClientError as e:
                    print(f"DynamoDB error removing from DB: {e}")
                    continue
        print('All done!')

    def _exists_in_db(self, stream_id: int) -> bool:
        """ Check if stream exists in DB """
        return int(stream_id) in [item['stream_id'] for item in self.saved]

    def _exists_in_streams(self, stream_id: int) -> bool:
        """ Check if stream exists in current streams """
        return int(stream_id) in [int(stream.id) for stream in self.streams]

    def _save_to_db(self, user: User, stream: Stream) -> None:
        """ Save stream to DB """
        self.db.put_item(**{
            'stream_id': int(stream.id),
            'user_login': user.login,
            'started_at': stream.started_at,
        })

    def _remove_from_db(self, stream_id: int) -> None:
        """ Remove stream from DB """
        self.db.delete_item('stream_id', int(stream_id))

