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
        Path(
            f'./channel_{channel_id}/playlists').mkdir(parents=True, exist_ok=True)
        playlists.to_csv(f'./channel_{channel_id}/playlists/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(id=playlist.id, title=playlist.title)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'./channel_{channel_id}/{playlist.title}.csv')
