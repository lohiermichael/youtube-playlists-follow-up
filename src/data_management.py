
import os
import json
import shutil
from pathlib import Path

from datetime import datetime
import pandas as pd

from authentication import Authentication
from models import Channel, Playlist

from config import FOLDER_CHANNELS, FOLDER_UPDATES, FOLDER_LOGS


def initialize_folders():
    """Build the structure of the folders
    """
    # Create the updates folder
    Path(FOLDER_UPDATES).mkdir(parents=True, exist_ok=True)

    # Create the channels folder
    Path(FOLDER_CHANNELS).mkdir(parents=True, exist_ok=True)

    # Create the logs folder
    Path(FOLDER_LOGS).mkdir(parents=True, exist_ok=True)

    # In the channels folder make a folder of new channel
    Path(f'{FOLDER_CHANNELS}/new_channel').mkdir(parents=True, exist_ok=True)

    # In the channels folder, initialize a file history_channels as an empty dictionary
    if not os.path.isfile(f'{FOLDER_CHANNELS}/history_channels.json'):
        with open(f'{FOLDER_CHANNELS}/history_channels.json', 'w') as f:
            json.dump({}, f)


def save_new_client_secrets(client_secrets_file):
    """Used when uploading a new client secrets file in the app
    """
    with open(f'{FOLDER_CHANNELS}/new_channel/clients_secrets', 'w') as f:
        json.dump(client_secrets_file, f)


def remove_files_empty_logs():
    if os.path.isfile(f'{FOLDER_UPDATES}/versions.txt'):
        with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f:
            latest_update = f.read().replace('\n', '')

    for log_file in os.listdir(FOLDER_LOGS):
        with open(f'{FOLDER_LOGS}/{log_file}', 'r') as f:
            dict_log = json.load(f)
        # If there is no logs for the update
        if not dict_log['logs'] and dict_log['log_time'] != latest_update:
            os.remove(f'{FOLDER_LOGS}/{log_file}')


def add_new_channel(mine: bool,
                    username: str = None,
                    new_client_secrets: bool = None,
                    channel_id_secrets: str = None):

    if new_client_secrets:
        authentication = Authentication(first_time=True,
                                        new_client_secrets=True)
    else:
        authentication = Authentication(first_time=True,
                                        new_client_secrets=False,
                                        channel_id_secrets=channel_id_secrets)

    if mine:
        channel = Channel(authentication=authentication,
                          mine=True,
                          build=True)

    elif username:
        channel = Channel(authentication=authentication,
                          username=username,
                          build=True)

    # Save information about the channel
    channel_info = {'title': channel.title,
                    'id': channel.id,
                    'published_at': channel.published_at,
                    'description': channel.description}

    with open(f'{FOLDER_CHANNELS}/{channel.id}/channel_info.json', 'w') as f:
        json.dump(channel_info, f)

    # Save the channel in history
    with open(f'{FOLDER_CHANNELS}/history_channels.json', 'r') as f_in:
        history_channels = json.load(f_in)

    history_channels[channel.id] = channel_info

    with open(f'{FOLDER_CHANNELS}/history_channels.json', 'w') as f_out:
        json.dump(history_channels, f_out)


def save_data(time: datetime = datetime.now(), first_time=True):
    method = 'w' if first_time else 'a'
    with open(f'{FOLDER_UPDATES}/versions.txt', method) as f:
        f.write(f'{str(time)}\n')

    Path(f'{FOLDER_UPDATES}/{time}').mkdir(parents=True, exist_ok=True)
    Path(f'{FOLDER_UPDATES}/{time}/channels').mkdir(parents=True, exist_ok=True)

    channels_ids = [channel_id for channel_id in next(
        os.walk(FOLDER_CHANNELS))[1] if channel_id != 'new_channel']

    for channel_id in channels_ids:
        authentication = Authentication(
            first_time=False, channel_id=channel_id)
        Path(
            f'{FOLDER_UPDATES}/{time}/channels/{channel_id}').mkdir(parents=True, exist_ok=True)
        channel = Channel(authentication=authentication,
                          id=channel_id, build=True)
        playlists = channel.playlists
        Path(
            f'{FOLDER_UPDATES}/{time}/channels/{channel_id}/playlists').mkdir(parents=True, exist_ok=True)
        playlists.to_csv(
            f'{FOLDER_UPDATES}/{time}/channels/{channel_id}/playlists.csv')
        for _, playlist in playlists.iterrows():
            playlist = Playlist(authentication=authentication,
                                id=playlist.id,
                                title=playlist.title,
                                build=True)
            playlist_items = playlist.items
            playlist_items.to_csv(
                f'{FOLDER_UPDATES}/{time}/channels/{channel_id}/playlists/{playlist.title}.csv', index=False)


def save_logs(logs: list):

    # Get the versions
    with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    log_time = versions[1].replace('\n', '')
    previous_update_time = versions[0].replace('\n', '')

    # Save the content of the file
    log_file_content = {'log_time': log_time,
                        'previous_update_time': previous_update_time, 'logs': logs}

    with open(f'{FOLDER_LOGS}/{log_time}.json', 'w') as f:
        json.dump(log_file_content, f)


def remove_old_version():

    with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f_in:
        versions = f_in.read().splitlines(True)

    old_version = versions[0].replace('\n', '')

    with open(f'{FOLDER_UPDATES}/versions.txt', 'w') as f_out:
        versions = f_out.write(versions[1])

    shutil.rmtree(f'{FOLDER_UPDATES}/{old_version}/')


def remove_all_data():

    shutil.rmtree(f'{FOLDER_UPDATES}/')
    Path('updates').mkdir(parents=True, exist_ok=True)
