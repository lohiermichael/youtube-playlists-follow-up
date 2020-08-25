
import os
import json
import shutil
from pathlib import Path

from datetime import datetime
import pandas as pd

from authentication import Authentication
from models import Channel, Playlist


def add_new_channel(mine: bool, username: str = None):

    # Ask if you want new credentials or use the credentials of previous channels
    new_client_secrets = False
    if new_client_secrets:
        authentication = Authentication(new_client_secrets=True)
    else:
        channel_id_cred = 'UCgJ4y17GAgzlLpqIJbj9gVQ'
        authentication = Authentication(
            new_client_secrets=False, channel_id=channel_id_cred)

    if mine:
        channel = Channel(authentication=authentication,
                          mine=True, build=True)

    elif username:
        channel = Channel(authentication=authentication,
                          username=username)

    # Save information about the channel
    channel_info = {'title': channel.title,
                    'id': channel.id,
                    'published_at': channel.published_at,
                    'description': channel.description}

    with open(f'channels/{channel.id}/channel_info.json', 'w') as f:
        json.dump(channel_info, f)


def save_data(time: datetime = datetime.now(), first_time=True):
    method = 'w' if first_time else 'a'
    with open('updates/versions.txt', method) as f:
        f.write(f'{str(time)}\n')

    Path(f'updates/{time}').mkdir(parents=True, exist_ok=True)
    Path(f'updates/{time}/channels').mkdir(parents=True, exist_ok=True)

    channels_ids = [channel_id for channel_id in os.listdir(
        'channels') if channel_id != 'new_channel']

    for channel_id in channels_ids:
        authentication = Authentication(
            new_client_secrets=False, channel_id=channel_id)
        Path(
            f'./updates/{time}/channels/{channel_id}').mkdir(parents=True, exist_ok=True)
        channel = Channel(authentication=authentication,
                          id=channel_id, build=True)
        playlists = channel.playlists
        Path(
            f'./updates/{time}/channels/{channel_id}/playlists').mkdir(parents=True, exist_ok=True)
        playlists.to_csv(
            f'./updates/{time}/channels/{channel_id}/playlists/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(authentication=authentication,
                                id=playlist.id,
                                title=playlist.title,
                                build=True)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'./updates/{time}/channels/{channel_id}/{playlist.title}.csv', index=False)


def save_logs(logs: list):

    # Create the log file if not already here
    Path(f'logs').mkdir(parents=True, exist_ok=True)

    # Get the versions
    with open('updates/versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    log_time = versions[1].replace('\n', '')
    previous_update_time = versions[0].replace('\n', '')

    # Save the content of the file
    log_file_content = {'log_time': log_time,
                        'previous_update_time': previous_update_time, 'logs': logs}

    with open(f'logs/{log_time}.json', 'w') as f:
        json.dump(log_file_content, f)


def remove_old_version():

    with open('updates/versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    old_version = versions[0].replace('\n', '')

    with open('updates/versions.txt', 'w') as f_out:
        versions = f_out.write(versions[1])

    shutil.rmtree(f'./updates/{old_version}/')


def remove_all_data():

    shutil.rmtree(f'./updates/')
    Path('updates').mkdir(parents=True, exist_ok=True)
