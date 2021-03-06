import json
import shutil

from compare_versions import run_comparison_workflow
from data_management import save_logs

from config import FOLDER_CHANNELS, FOLDER_UPDATES


class LogsCreation:
    def __init__(self, file_comparison):
        self.file_comparison = file_comparison

        with open(file_comparison, 'r') as f:
            self.dict_res_comparison = json.load(f)

        self.logs = []

        self._store_playlist_messages()

        self._store_item_messages()

        self._store_channel_messages()

    def _store_channel_messages(self):
        # Old channels
        for _, channel_info in self.dict_res_comparison['old_channels'].items():
            channel_title = channel_info['title']
            message = f'You stopped following the channel {channel_title}'
            self.logs.append(
                {'message': message, 'type': 'remove_channel',
                    'channel_title': channel_title}
            )

        # New channels
        for _, channel_info in self.dict_res_comparison['new_channels'].items():
            channel_title = channel_info['title']
            message = f'You are now following the channel {channel_title}'
            self.logs.append(
                {'message': message, 'type': 'create_channel',
                    'channel_title': channel_title}
            )

    def _store_playlist_messages(self):
        # Loop over the common channels
        for channel_name, common_chanel in self.dict_res_comparison['common_channels'].items():
            # Old playlists
            if common_chanel['old_playlists']:
                for playlist_name, playlist in common_chanel['old_playlists'].items():
                    message = f'The playlist {playlist_name} has been removed.'
                    self.logs.append(
                        {'message': message, 'type': 'remove_playlist', 'playlist_name': playlist_name})
                    # Loop over items in the created playlist
                    if playlist:
                        for item_id, item in playlist['items'].items():
                            item_title = item['title']
                            message = f'The video {item_title} has been removed from the playlist {playlist_name} because the playlist {playlist_name} has been removed.'
                            self.logs.append(
                                {'message': message, 'type': 'remove_item', 'item_title': item_title, 'playlist_name': playlist_name})

            # New playlists
            if common_chanel['new_playlists']:
                for playlist_name, playlist in common_chanel['new_playlists'].items():
                    message = f'The playlist {playlist_name} has been created.'
                    self.logs.append(
                        {'message': message, 'type': 'create_playlist'})
                    # Loop over items in the created playlist
                    if playlist:
                        for item_id, item in playlist['items'].items():
                            item_title = item['title']
                            message = f'The video {item_title} has been added to the playlist {playlist_name}.'
                            self.logs.append(
                                {'message': message, 'type': 'create_item', 'item_title': item_title, 'playlist_name': playlist_name})

    def _store_item_messages(self):

        # Loop over the common channels
        for channel_name, common_chanel in self.dict_res_comparison['common_channels'].items():
            # Loop over the common playlists
            for playlist_name, common_playlist in common_chanel['common_playlists'].items():
                # Old items
                if common_playlist['old_items']:
                    for item_id, item in common_playlist['old_items'].items():
                        item_title = item['title']
                        message = f'The video {item_title} has been removed from the playlist {playlist_name}.'
                        self.logs.append(
                            {'message': message, 'type': 'remove_item', 'item_title': item_title, 'playlist_name': playlist_name})
                # New items
                if common_playlist['new_items']:
                    for item_id, item in common_playlist['new_items'].items():
                        item_title = item['title']
                        message = f'The video {item_title} has been added to the playlist {playlist_name}.'
                        self.logs.append(
                            {'message': message, 'type': 'add_item', 'item_title': item_title, 'playlist_name': playlist_name})


def run_logs_workflow():
    print('\n')
    print('Results:')
    print('\n')
    logs = LogsCreation(f'{FOLDER_UPDATES}/comparison_results.json').logs
    for log in logs:
        print(log['message'])
    print('\n')

    save_logs(logs=logs)
