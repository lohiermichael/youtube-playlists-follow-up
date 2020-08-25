import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors


class Authentication:
    def __init__(self,
                 auth_type,
                 api_key=None,
                 scopes=["https://www.googleapis.com/auth/youtube.readonly"],
                 oauth_credentials_file='OAUTH_CREDENTIALS',
                 client_secrets_file='client_secret.json',
                 api_service_name='youtube',
                 api_version='v3'):
        """Authentication strategy

        Args:
            auth_type ([str]): Either 'own_account' for strong rights authentication or 'other_account' for light one
                               'own_account' requires OAuth 2.0 authentication and 'other_account' only an API Key on Google Cloud 
            api_key ([str], optional): For the 'other_account' type of authentication. Defaults to None.
            scope (list, optional): Google attribute we shouldn't be changing. Defaults to ["https://www.googleapis.com/auth/youtube.readonly"].
            client_secrets_file (str, optional): JSON file that stores the client credentials to get the OAuth credentils. Defaults to 'client_secret.json'.
            oauth_credentials_file (str, optional): Pickle file in which we will store the OAuth credentials. Defaults to 'oauth_credentials.json'
            api_service_name (str, optional): Google attribute we shouldn't be changing. Defaults to 'youtube'.
            api_version (str, optional): Google attribute we shouldn't be changing. Defaults to 'v3'.
        """

        self.api_key = api_key
        self.scopes = scopes
        self.client_secrets_file = client_secrets_file
        self.oauth_credentials_file = oauth_credentials_file
        self.api_service_name = api_service_name
        self.api_version = api_version

        assert auth_type in ['own_account', 'other_account']

        if auth_type == 'other_account':
            self._get_authenticated_api_key()
        elif auth_type == 'own_account':
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
        if os.path.exists(self.oauth_credentials_file):
            with open(self.oauth_credentials_file, 'rb') as f:
                self.credentials = pickle.load(f)

        # If not request them
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file,
                                                             self.scopes)
            self.credentials = flow.run_local_server()
            with open(self.oauth_credentials_file, 'wb') as f:
                pickle.dump(self.credentials, f)

        # Make the youtube object with the credentials
        self.youtube = build(self.api_service_name,
                             self.api_version,
                             credentials=self.credentials)


if __name__ == "__main__":
    own_auth = Authentication(auth_type='own_account')
    normal_auth = Authentication(auth_type='other_account')

    youtube = normal_auth.youtube
    request = youtube.channels().list(
        part='snippet',
        forUsername=os.environ['YOUTUBE_USERNAME']
    )
    response = request.execute()

    print(response)

    youtube = own_auth.youtube
    request = youtube.channels().list(
        part='snippet',
        mine=True
    )
    response = request.execute()

    print(response)
