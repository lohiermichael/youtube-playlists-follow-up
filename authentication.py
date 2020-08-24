import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors


class Authentication:
    def __init__(self,
                 auth_type,
                 api_key=None
                 scope=["https://www.googleapis.com/auth/youtube.readonly"],
                 client_secrets_file='client_secret.json',
                 api_service_name='youtube',
                 api_version='v3'):

        self.api_key = api_key
        self.scope = scope
        self.client_secrets_file = client_secrets_file
        self.api_service_name = api_service_name
        self.api_version = api_version

        assert auth_type in ['own_account', 'other_account']

        if auth_type == 'own_account':
            self._get_authenticated_api_key()
        elif auth_type == 'other_account':
            self._get_authenticated_oauth_2()

    def _get_authenticated_api_key(self):
        """Make the youtube identifier object"""

        self.api_key = os.environ['PROJECT_API_KEY']

        self.youtube = build(serviceName=self.api_service_name,
                             version=self.api_version,
                             developerKey=self.api_key)

    def _get_authenticated_oauth_2(self):
        """Make the youtube identifier object with OAuth """

        # If the credentials are already present, get them locally
        if os.path.exists("CREDENTIALS_PICKLE_FILE"):
            with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
                self.credentials = pickle.load(f)

        # If not request them
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server()
            with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
                pickle.dump(credentials, f)

        # Make the youtube object with the credentials
        self.youtube = build(api_service_name, api_version,
                             credentials=credentials)


if __name__ == "__main__":
    a = Authentication(auth_type='own_account')
