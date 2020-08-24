
import os
import json
import shutil
from pathlib import Path

from datetime import datetime
import pandas as pd

from models import Channel, Playlist, User


def save_data(first_time: bool, time: datetime = datetime.now()):
    method = 'w' if first_time else 'a'
    with open('versions.txt', method) as f:
        f.write(f'{str(time)}\n')

    Path(f'{time}').mkdir(parents=True, exist_ok=True)
    user = User(name=os.environ['YOUTUBE_USERNAME'])
    for channel_id in user.channels_ids:
        Path(f'./{time}/channel_{channel_id}').mkdir(parents=True, exist_ok=True)
        channel = Channel(id=channel_id, build=True)
        playlists = channel.playlists
        Path(
            f'./{time}/channel_{channel_id}/playlists').mkdir(parents=True, exist_ok=True)
        playlists.to_csv(
            f'./{time}/channel_{channel_id}/playlists/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(
                id=playlist.id, title=playlist.title, build=True)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'./{time}/channel_{channel_id}/{playlist.title}.csv', index=False)


def save_logs(logs: list):

    # Create the log file if not already here
    Path(f'logs').mkdir(parents=True, exist_ok=True)

    # Get the versions
    with open('versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    log_time = versions[1].replace('\n', '')
    previous_update_time = versions[0].replace('\n', '')

    # Save the content of the file
    log_file_content = {'log_time': log_time,
                        'previous_update_time': previous_update_time, 'logs': logs}

    with open(f'logs/{log_time}.json', 'w') as f:
        json.dump(log_file_content, f)


def remove_old_version():

    with open('versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    old_version = versions[0].replace('\n', '')

    with open('versions.txt', 'w') as f_out:
        versions = f_out.write(versions[1])

    shutil.rmtree(f'./{old_version}/')


def remove_all_data():

    with open('versions.txt', 'r') as f:
        versions = f.read().splitlines(True)

    # Remove old and updated version
    for version in versions:
        version = version.replace('\n', '')
        shutil.rmtree(f'./{version}/')

    os.remove('versions.txt')


if __name__ == "__main__":
    saved_logs()
