from typing import List, Optional

import twitch
from twitch.helix.models.user import User

from streamingbot.slack import SlackHandler


class StreamingBot:
    """ Streamingbot yay! """
    def __init__(self, twitch_client_id: str, slack_webhook_url: str) -> None:
        self.tw = twitch.Helix(twitch_client_id)   # Twitch session
        self.sl = SlackHandler(slack_webhook_url)  # Slack session
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
        for streamer in streamers:
            resp = self.sl.send_message(streamer)
            print(
                f"Sent message to Slack for {streamer.login} with result: "
                f"{resp.status_code} {resp.text}"
            )

