

import os
from googleapiclient.discovery import build
import json
import pandas as pd

api_key = os.environ['PROJECT_API_KEY']
username = os.environ['YOUTUBE_USERNAME']

global youtube
youtube = build(serviceName='youtube',
                version='v3',
                developerKey=api_key)


class Channel:
    def __init__(self, id):
        self.id = id
        self.playlists = self._get_playlists()

    def _get_playlists(self) -> pd.DataFrame:
        # List playlists of my channel
        request = youtube.playlists().list(
            part='snippet',
            channelId=os.environ['CHANNEL_ID'],
            maxResults=50
        )
        response = request.execute()

        playlists = [playlist['snippet'] for playlist in response['items']]
        df_playlists = pd.DataFrame.from_records(playlists)
        df_playlists['id'] = [playlist['id'] for playlist in response['items']]
        channel_id = df_playlists['channelId'].iloc[0]

        df_playlists = df_playlists[['id', 'title', 'publishedAt']]

        return df_playlists


class User:
    def __init__(self, name):
        self.name = name
        self.channels_ids = self._get_channels_ids()

    def _get_channels_ids(self) -> list:
        request = youtube.channels().list(
            part='snippet',
            forUsername=os.environ['YOUTUBE_USERNAME']
        )
        response = request.execute()

        return [channel['id'] for channel in response['items']]


if __name__ == '__main__':
    # List all my channels
    me = User(name=os.environ['YOUTUBE_USERNAME'])
    channels_id = me.channels_ids[0]
    my_channel = Channel(id=channels_id)
    playlist_test = my_channel.playlists.iloc[0]
    print(playlist_test)
