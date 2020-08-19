import json
from compare_versions import run_comparison_workflow


class Logs:
    def __init__(self, file_comparison):
        self.file_comparison = file_comparison

        with open(file_comparison, 'r') as f:
            self.dict_res_comparison = json.load(f)

        self.logs = []

        self.make_item_messages()

    def make_item_messages(self):

        # Loop over the common channels
        for channel_name, common_chanel in self.dict_res_comparison['common_channels'].items():
            # Loop over the common playlists
            for playlist_name, common_playlist in common_chanel['common_playlists'].items():
                # Old items
                if common_playlist['old_items']:
                    for item_id, item in common_playlist['old_items'].items():
                        item_title = item['title']
                        message = f'The video {item_title} has been removed from the playlist {playlist_name}'
                        self.logs.append(
                            {'message': message, 'type': 'removed_item'})
                # New items
                if common_playlist['new_items']:
                    for item_id, item in common_playlist['new_items'].items():
                        item_title = item['title']
                        message = f'The video {item_title} has been added to the playlist {playlist_name}'
                        self.logs.append(
                            {'message': message, 'type': 'added_item'})


if __name__ == '__main__':
    # run_comparison_workflow()
    print('\n')
    print('Results:')
    print('\n')
    logs = Logs('comparison_results.json').logs
    for log in logs:
        print(log['message'])
