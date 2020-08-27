import os
import json
import shutil
from datetime import datetime

from googleapiclient.discovery import build
import pandas as pd

from authentication import Authentication

from config import FOLDER_UPDATES, FOLDER_LOGS, FOLDER_UPDATES


class Channel:
    def __init__(self,
                 authentication: Authentication,
                 id=None,
                 username=None,
                 mine: bool = True,
                 update_time=None,
                 build=False):

        self.youtube = authentication.youtube
        self.id = id
        self.username = username
        self.mine = mine

        assert self.username or self.mine, "You need a username or set that it is your channel to create a Channel"

        if build:

            if mine:
                self.api_response = self._get_info_your_channel()

            elif self.username:
                self.api_response = self._get_info_by_user_name()

            self.id = self.api_response['items'][0]['id']
            self.published_at = self.api_response['items'][0]['snippet']['publishedAt']
            self.description = self.api_response['items'][0]['snippet']['description']
            self.title = self.api_response['items'][0]['snippet']['title']

            self.playlists = self._get_playlists()

        else:  # Already stored
            self.update_time = update_time
            self.playlists = pd.read_csv(
                f'{FOLDER_UPDATES}/{self.update_time}/channels/{self.id}/playlists/playlists.csv')

    def __iter__(self):
        return [Playlist(id=playlist['id'],
                         title=playlist['title'],
                         of_channel=self)
                for _, playlist in self.playlists.iterrows()].__iter__()

    def __repr__(self):
        playlists_str = ', '.join(self.playlists['title'])
        return f'Channel(playlists({playlists_str}))'

    def _get_info_by_user_name(self) -> dict:

        request = self.youtube.channels().list(
            part='snippet',
            forUsername=self.username
        )
        response = request.execute()

        return response

    def _get_info_your_channel(self) -> dict:

        request = self.youtube.channels().list(
            part='snippet',
            mine=True
        )
        response = request.execute()

        return response

    def _get_playlists(self) -> pd.DataFrame:
        # List playlists of my channel
        request = self.youtube.playlists().list(
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
    def __init__(self, id, authentication: Authentication, title, of_channel: Channel = None, build=False):
        self.youtube = authentication.youtube
        self.id = id
        self.title = title
        if build:
            self.items = self._get_items()
        else:  # Already stored
            self.of_channel = of_channel
            self.update_time = of_channel.update_time
            self.items = pd.read_csv(
                f'{FOLDER_UPDATES}/{self.update_time}/channels/{self.of_channel.id}/{self.title}.csv')

    def __repr__(self):
        items_str = len(self.items)
        return f'Playlist(title: "{self.title}", items: ({len(self.items)}))'

    def _get_items(self) -> pd.DataFrame:

        df_videos = pd.DataFrame(columns=[
            'id', 'title', 'publishedAt', 'description'])
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
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


class LogsByUpdate(list):
    """Reconstitute Logs from saved files"""

    def __init__(self):

        if not os.listdir(FOLDER_LOGS):
            self.update_times = []

        else:
            self.update_times = [update_time.replace(
                '.json', '') for update_time in os.listdir(FOLDER_LOGS)]

            # Put the latest first
            self.update_times.sort(reverse=True)

            for update_time in self.update_times:
                with open(f'{FOLDER_LOGS}/{update_time}.json') as f:
                    logs_for_update = json.load(f)
                self.append(logs_for_update)


class LatestData():
    def __init__(self):
        # Remove any possible old folder of data
        if 'versions.txt' not in os.listdir(FOLDER_UPDATES):
            shutil.rmtree(FOLDER_UPDATES)
            raise Exception('versions.txt was not present in the files')
        if not os.listdir(FOLDER_LOGS):
            shutil.rmtree(FOLDER_LOGS)
            raise Exception(
                "We can't get the latest data as the log file is empty")

            self.channels = []
            self.update_time = None
            self.previous_update_time = None

        else:

            with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f:
                self.update_time = f.read().replace('\n', '')

            with open(f'{FOLDER_LOGS}/{self.update_time}.json', 'r') as f:
                self.previous_update_time = json.load(
                    f)['previous_update_time']

            self.channels = [Channel(id=channel.replace('channel_', ''),
                                     build=False,
                                     update_time=self.update_time)
                             for channel in os.listdir(f'{FOLDER_UPDATES}/{self.update_time}')]


if __name__ == "__main__":
    l = LatestData()
    print(l.channels)
