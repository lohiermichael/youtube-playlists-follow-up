import json
import shutil

from compare_versions import run_comparison_workflow
from data_management import save_logs


class Logs:
    def __init__(self, file_comparison):
        self.file_comparison = file_comparison

        with open(file_comparison, 'r') as f:
            self.dict_res_comparison = json.load(f)

        self.logs = []

        self._store_playlist_messages()

        self._store_item_messages()

    def _store_playlist_messages(self):
        # Loop over the common channels
        for channel_name, common_chanel in self.dict_res_comparison['common_channels'].items():
            # Old playlists
            if common_chanel['old_playlists']:
                for playlist_name, playlist in common_chanel['old_playlists'].items():
                    message = f'The playlist {playlist_name} has been removed.'
                    self.logs.append(
                        {'message': message, 'type': 'remove_playlist'})
                    # Loop over items in the created playlist
                    if playlist:
                        for item_id, item in playlist['items'].items():
                            item_title = item['title']
                            message = f'The video {item_title} has been removed from the playlist {playlist_name} because the playlist {playlist_name} has been removed.'
                            self.logs.append(
                                {'message': message, 'type': 'remove_item'})

            # New
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
                                {'message': message, 'type': 'create_item'})

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
                            {'message': message, 'type': 'remove_item'})
                # New items
                if common_playlist['new_items']:
                    for item_id, item in common_playlist['new_items'].items():
                        item_title = item['title']
                        message = f'The video {item_title} has been added to the playlist {playlist_name}.'
                        self.logs.append(
                            {'message': message, 'type': 'add_item'})


def run_logs_workflow():
    print('\n')
    print('Results:')
    print('\n')
    logs = Logs('comparison_results.json').logs
    for log in logs:
        print(log['message'])
    print('\n')

    save_logs(logs=logs)
