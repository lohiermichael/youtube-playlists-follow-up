
import os
from pathlib import Path

from datetime import datetime
import pandas as pd

from objects import Channel, Playlist, User


def save_data(first_time: bool, time: datetime = datetime.now()):
    method = 'w' if first_time else 'a'
    with open('versions.txt', method) as f:
        f.write(f'{str(time)}\n')

    Path(f'{time}').mkdir(parents=True, exist_ok=True)
    user = User(name=os.environ['YOUTUBE_USERNAME'])
    for channel_id in user.channels_ids:
        Path(f'./{time}/channel_{channel_id}').mkdir(parents=True, exist_ok=True)
        channel = Channel(id=channel_id)
        playlists = channel.playlists
        Path(
            f'./{time}/channel_{channel_id}/playlists').mkdir(parents=True, exist_ok=True)
        playlists.to_csv(
            f'./{time}/channel_{channel_id}/playlists/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(id=playlist.id, title=playlist.title)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'./{time}/channel_{channel_id}/{playlist.title}.csv')
