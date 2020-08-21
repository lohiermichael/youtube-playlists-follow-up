import os
import json

from googleapiclient.discovery import build
import pandas as pd


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
    def __init__(self, id, update_time=None, build=False):
        self.id = id
        if build:
            self.playlists = self._get_playlists()
        else:  # Already stored
            self.update_time = update_time
            self.playlists = pd.read_csv(
                f'{self.update_time}/channel_{self.id}/playlists/playlists.csv')

    def __iter__(self):
        return [Playlist(id=playlist['id'],
                         title=playlist['title'],
                         of_channel=self)
                for _, playlist in self.playlists.iterrows()].__iter__()

    def __repr__(self):
        playlists_str = ', '.join(self.playlists['title'])
        return f'Channel(playlists({playlists_str}))'

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


class Playlist():
    def __init__(self, id, title, of_channel: Channel = None, build=False):
        self.id = id
        self.title = title
        if build:
            self.items = self._get_items()
        else:  # Already stored
            self.of_channel = of_channel
            self.update_time = of_channel.update_time
            self.items = pd.read_csv(
                f'{self.update_time}/channel_{self.of_channel.id}/{self.title}.csv')

    def __repr__(self):
        items_str = len(self.items)
        return f'Playlist(title: "{self.title}", items: ({len(self.items)}))'

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


class Logs(dict):
    """Reconstitute Logs from saved files"""

    def __init__(self):
        self.update_times = [update_time.replace(
            '.json', '') for update_time in os.listdir('Logs')]

        self.keys = self.update_times
        for update_time in self.keys:
            with open(f'logs/{update_time}.json') as f:
                logs_for_update = json.load(f)
            self[update_time] = logs_for_update

        print(self)


class LatestData():
    def __init__(self):

        with open('versions.txt', 'r') as f:
            self.update_time = f.read().replace('\n', '')

        with open(f'logs/{self.update_time}.json', 'r') as f:
            self.previous_update_time = json.load(f)['previous_update_time']

        self.channels = [Channel(id=channel.replace('channel_', ''),
                                 build=False,
                                 update_time=self.update_time)
                         for channel in os.listdir(f'{self.update_time}')]


if __name__ == "__main__":
    ld = LatestData()
    print(ld.channels)
    for channel in ld.channels:
        for playlist in channel:
            print('\n')
            print(playlist)
