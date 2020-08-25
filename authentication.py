import os
import pickle
from pathlib import Path


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors


class Authentication:
    def __init__(self,
                 new_client_secrets: bool = True,
                 channel_id: str = None,
                 client_secrets_file: str = 'channels/new_channel/client_secret.json'):
        """Will save in the files the auth credentials if not already done.
        The important object of Authentication is youtube, which will allow you to request the Youtube data  API.

        Args:
            first_time (bool): If set to True, it will request an access to your channel. Defaults to True.
            channel_id (str, optional): If first_time is False, it will get the authentication from the saved files under channel Id. Defaults to None if first_time is True.
        """

        self.channel_id = channel_id

        if self.channel_id:
            self.client_secrets_file = f'channels/{channel_id}/client_secrets.json'

        # The file of the credentials from which the channel has been created if already exists
        # It is temporarily saved under new channel, as we don't know the channel id yes
        self.client_secrets_file = f'channels/new_channel/client_secrets.json'

        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        self.api_service_name = 'youtube'
        self.api_version = 'v3'

        if new_client_secrets:
            self._get_authenticated_first_time()
            # Move the client_secrets_file under its channel id folder
            new_destination = f'channels/{self.channel_id}/client_secrets.json'
            os.rename(self.client_secrets_file, new_destination)
            self.client_secrets_file = new_destination

        else:
            self._get_authenticated_from_file()

    def _get_authenticated_first_time(self):

        # Ask for authorization
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file,
                                                         self.scopes)
        # Get the credentials
        self.credentials = flow.run_local_server()

        # Make the Youtube object
        self._make_youtube_object()

        # Save the credentials in a file

        # Get the channel id
        request = self.youtube.channels().list(
            part='snippet',
            mine='True'
        )
        response = request.execute()

        self.channel_id = response['items'][0]['id']

        # Create a new folder for the channel
        Path(f'channels/{self.channel_id}').mkdir(parents=True, exist_ok=True)

        # Save the credentials in a file called OAUTH_CREDENTIALS
        self.oauth_credentials_file = f'channels/{self.channel_id}/OAUTH_CREDENTIALS'

        with open(self.oauth_credentials_file, 'wb') as f:
            pickle.dump(self.credentials, f)

    def _get_authenticated_from_file(self):

        self.oauth_credentials_file = f'channels/{self.channel_id}/OAUTH_CREDENTIALS'

        with open(self.oauth_credentials_file, 'rb') as f:
            self.credentials = pickle.load(f)

        self._make_youtube_object()

    def _make_youtube_object(self):
        self.youtube = build(self.api_service_name,
                             self.api_version,
                             credentials=self.credentials)
