from typing import List, Optional

from botocore.exceptions import ClientError

import twitch
from twitch.helix.models.user import User

from streamingbot.db import DynamoDBHandler
from streamingbot.slack import SlackHandler


DB_NAME = 'streamingbotdb'


class StreamingBot:
    """ Streamingbot yay! """
    def __init__(self, twitch_client_id: str, slack_webhook_url: str) -> None:
        self.tw = twitch.Helix(twitch_client_id)   # Twitch session
        self.sl = SlackHandler(slack_webhook_url)  # Slack session
        self.db = DynamoDBHandler(DB_NAME)         # DynamoDB session
        self.users: Optional[List[User]] = []      # Twitch users to watch

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

        print(f"{len(self.users)} in my list")

        # Get a list of live streamers
        streamers = []
        for user in self.users:
            if user.is_live:
                print(f"{user.login} is live!")
                streamers.append(user)
            else:
                print(f"{user.login} is not streaming")

        # Process the streamers
        for user in streamers:
            try:
                # First check if stream is already in DB
                if self._exists_in_db(user.stream.id):
                    print(
                        f"I am already aware of {user.login}'s stream "
                        f"(ID: {user.stream.id}) - skipping Slack messaging"
                    )
                    continue

                # Save to DB
                print(f"{user.login}'s stream (ID: {user.stream.id}) is new!")
                self._save_to_db(user)
                print(f"Stream {user.stream.id} saved to DB")

                # Send to Slack
                resp = self.sl.send_message(user)
                print(
                    f"Sent message to Slack for {user.login} with result: "
                    f"{resp.status_code} {resp.text}"
                )
            except ClientError as e:
                print(f"DYNAMODB ERROR: {e}")
                continue

    def _exists_in_db(self, stream_id: int) -> bool:
        """ Check if stream exists in DB """
        return bool(self.db.get_item('stream_id', int(stream_id)))

    def _save_to_db(self, user: User) -> None:
        """ Save stream to DB """
        self.db.put_item(**{
            'stream_id': int(user.stream.id),
            'user_login': user.login,
            'started_at': user.stream.started_at,
        })

    def _remove_from_db(self, stream_id: int) -> None:
        """ Remove stream from DB """
        self.db.delete_item('stream_id', int(stream_id))

