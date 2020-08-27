import os
import pickle
from shutil import copyfile
from pathlib import Path


from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors

from config import FOLDER_CHANNELS


class Authentication:
    def __init__(self,
                 first_time: bool = None,
                 new_client_secrets: bool = None,
                 channel_id_secrets: str = None,
                 channel_id: str: None):

        # Conditions on the inputs: there are three cases
    self.case_first_time_reuse_secrets = first_time and not new_client_secrets and channel_id_secrets
    self.case_first_time_new_secrets = first_time and new_client_secrets
    self.case_already_stored = not first_time

    assert self.case_first_time_reuse_secrets or self.case_first_time_new_secrets or self.case_already_stored, "You are not initializing the inputs correctly"

    self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    self.api_service_name = 'youtube'
    self.api_version = 'v3'

    self.first_time = first_time
    self.new_client_secrets = new_client_secrets
    self.channel_id_secrets = channel_id_secrets
    self.channel_id = channel_id
    self.client_secrets_file = self._define_client_secrets_file()

    if self.first_time:
        self._get_authenticated_first_time()
        self._move_client_secrets_file()
    else:
        self._get_authenticated_from_file()

    def _define_client_secrets_file(self):

        if self.case_first_time_reuse_secrets:
            return f'{FOLDER_CHANNELS}/{self.channel_id_secrets}/client_secrets.json'
        elif self.case_first_time_new_secrets:
            return f'{FOLDER_CHANNELS}/new_channel/client_secrets.json'
        elif self.case_already_stored:
            return f'{FOLDER_CHANNELS}/{channel_id}/client_secrets.json'

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
        Path(f'{FOLDER_CHANNELS}/{self.channel_id}').mkdir(parents=True, exist_ok=True)

        # Save the OAuth credentials in a file called OAUTH_CREDENTIALS
        self.oauth_credentials_file = f'{FOLDER_CHANNELS}/{self.channel_id}/OAUTH_CREDENTIALS'

        with open(self.oauth_credentials_file, 'wb') as f:
            pickle.dump(self.credentials, f)

    def _move_client_secrets_file(self):

        new_destination = f'{FOLDER_CHANNELS}/{self.channel_id}/client_secrets.json'

        # In this case we move the file
        if self.case_first_time_new_secrets:
            os.rename(self.client_secrets_file, new_destination)

        # In this case we copy the file
        elif self.case_first_time_reuse_secrets:
            copyfile(self.client_secrets_file, new_destination)

        # Redefine the new location
        self.client_secrets_file = new_destination

    def _get_authenticated_from_file(self):

        self.oauth_credentials_file = f'{FOLDER_CHANNELS}/{self.channel_id}/OAUTH_CREDENTIALS'

        with open(self.oauth_credentials_file, 'rb') as f:
            self.credentials = pickle.load(f)

        self._make_youtube_object()

    def _make_youtube_object(self):
        self.youtube = build(self.api_service_name,
                             self.api_version,
                             credentials=self.credentials)
