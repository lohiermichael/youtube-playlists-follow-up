from googleapiclient.discovery import build
import pandas as pd
import os

api_key = os.environ['PROJECT_API_KEY']
username = os.environ['YOUTUBE_USERNAME']

global youtube
youtube = build(serviceName='youtube',
                version='v3',
                developerKey=api_key)


class User:
    def __init__(self, name):
        self.name = name
        self.channels_ids = self._get_channels_ids()

    def _get_channels_ids(self) -> list:
        request = youtube.channels().list(
            part='snippet',
            forUsername=self.name
        )
        response = request.execute()

        return [channel['id'] for channel in response['items']]


class Channel:
    def __init__(self, id):
        self.id = id
        self.playlists = self._get_playlists()

    def _get_playlists(self) -> pd.DataFrame:
        # List playlists of my channel
        request = youtube.playlists().list(
            part='snippet',
            channelId=self.id,
            maxResults=50
        )
        response = request.execute()

        playlists = [playlist['snippet'] for playlist in response['items']]
        df_playlists = pd.DataFrame.from_records(playlists)
        df_playlists['id'] = [playlist['id'] for playlist in response['items']]
        df_playlists = df_playlists[['id', 'title', 'publishedAt']]

        return df_playlists


class Playlist:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.items = self._get_items()

    def _get_items(self) -> pd.DataFrame:

        df_videos = pd.DataFrame(columns=[
            'id', 'title', 'publishedAt', 'description'])
        next_page_token = None

        while True:
            request = youtube.playlistItems().list(
                part='snippet',
                playlistId=self.id,
                maxResults=50,
                pageToken=next_page_token
            )
            chunk_response = request.execute()

            videos = [video['snippet'] for video in chunk_response['items']]

            # The playlist is empty
            if not videos:
                break

            df_chunk_videos = pd.DataFrame.from_records(videos)
            df_chunk_videos['id'] = [video['id']
                                     for video in chunk_response['items']]
            df_chunk_videos = df_chunk_videos[[
                'id', 'title', 'publishedAt', 'description']]

            df_videos = df_videos.append(df_chunk_videos)

            next_page_token = chunk_response.get('nextPageToken')

            if not next_page_token:
                break

        return df_videos
