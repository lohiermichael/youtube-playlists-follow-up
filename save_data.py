from objects import Channel, Playlist, User
import os
from pathlib import Path
import pandas as pd


if __name__ == '__main__':
    # Make directory for channels
    user = User(name=os.environ['YOUTUBE_USERNAME'])
    for channel_id in user.channels_ids:
        Path(f'./channel_{channel_id}').mkdir(parents=True, exist_ok=True)
        channel = Channel(id=channel_id)
        # Make a file with all playlists in the channel
        playlists = channel.playlists
        playlists.to_csv(f'./channel_{channel_id}/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(id=playlist.id, title=playlist.title)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'./channel_{channel_id}/{playlist.title}.csv')


# # Make
# playlists.to_csv('playlists.csv')

# playlist_test_id = playlists[playlists['title']
#                              == 'Jazz music']['id'].item()
# # print(playlist_test_id)
# playlist_test = Playlist(id=playlist_test_id)
# items_test = playlist_test.items
# print(len(items_test))
# items_test.to_csv('items.csv')

# with open('res.json', 'w') as f:
#     json.dump(response, f)
