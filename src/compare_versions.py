import os
import shutil
import json
from typing import Tuple

from datetime import datetime
from time import sleep
import pandas as pd

from data_management import save_data
from config import FOLDER_UPDATES, FOLDER_CHANNELS


def make_summary(old_L: list, new_L: list, print_of: bool = True) -> Tuple[list]:
    common_elements = [element for element in old_L if element in new_L]
    elements_old_only = [
        element for element in old_L if element not in new_L]
    elements_new_only = [
        element for element in new_L if element not in old_L]

    # Summary
    if print_of:
        print(f'In common: {len(common_elements)}')
        print(common_elements)
        print('\n')
        print(f'In old and not in new: {len(elements_old_only)}')
        print(elements_old_only)
        print('\n')
        print(f'In new and not in old: {len(elements_new_only)}')
        print(elements_new_only)
        print('\n')

    return common_elements, elements_old_only, elements_new_only


class CompareVersions:
    def __init__(self, old_version, new_version):
        self.old_version = old_version
        self.new_version = new_version
        self.summary = {}
        self._run_comparisions()

    def _run_comparisions(self):
        print('Compare channels')
        self.compare_channels()
        self._save_comparison_results()
        print('Compare playlists')
        self.compare_playlists()
        self._save_comparison_results()
        print('Compare playlist items')
        self.compare_common_playlist_items()
        self._save_comparison_results()

    def _save_comparison_results(self):
        with open(f'{FOLDER_UPDATES}/comparison_results.json', 'w') as f:
            json.dump(self.summary, f)

    def compare_channels(self):
        self.old_channels = os.listdir(
            f'{FOLDER_UPDATES}/{self.old_version}/channels')
        self.new_channels = os.listdir(
            f'{FOLDER_UPDATES}/{self.new_version}/channels')

        self.summary['common_channels'], self.summary['old_channels'], self.summary['new_channels'] = make_summary(
            old_L=self.old_channels, new_L=self.new_channels, print_of=False)

        # Store elements old channels
        self.store_details_channels(type_channels='old_channels')

        # Store new channels
        self.store_details_channels(type_channels='new_channels')

    def store_details_channels(self, type_channels: str):

        if type_channels == 'old_channels':
            list_channels = self.old_channels
            version = self.old_version
        elif type_channels == 'new_channels':
            list_channels = self.new_channels
            version = self.new_version
        else:
            raise AttributeError(
                f"{type_channels} does not exist, it must be  'old_channels' or 'new_channels'")

        # Store the old channel names
        list_channels = self.summary[type_channels]
        self.summary[type_channels] = {}

        # Store the playlists
        for channel_id in list_channels:
            with open(f'{FOLDER_CHANNELS}/history_channels.json', 'r') as f:
                history_channels = json.load(f)
            self.summary[type_channels][channel_id] = history_channels[channel_id]

    def compare_playlists(self):

        # Playlists in common
        self.compare_common_playlists()

        # Store elements old playlists
        self.store_all_elements_playlists(type_playlists='old_playlists')

        # Store elements old playlists
        self.store_all_elements_playlists(type_playlists='new_playlists')

    def store_all_elements_playlists(self, type_playlists: str):
        if type_playlists == 'old_playlists':
            version = self.old_version
        elif type_playlists == 'new_playlists':
            version = self.new_version
        else:
            raise AttributeError(
                f"{type_playlists} does not exist, it must be  'old_playlists' or 'new_playlists'")

        for common_channel in self.summary['common_channels']:
            list_playlists = self.summary['common_channels'][common_channel][type_playlists]
            self.summary['common_channels'][common_channel][type_playlists] = {}
            for playlist in list_playlists:
                self.summary['common_channels'][common_channel][type_playlists][playlist] = {
                }
                df_playlist = pd.read_csv(
                    f'./{version}/{common_channel}/{playlist}.csv')
                self.summary['common_channels'][common_channel][type_playlists][playlist]['items'] = df_playlist.T.to_dict(
                )

    def compare_common_playlists(self):

        list_common_channels = self.summary['common_channels']
        self.summary['common_channels'] = {}

        for channel in list_common_channels:
            self.summary['common_channels'][channel] = {}
            old_playlists = os.listdir(
                f'{FOLDER_UPDATES}/{self.old_version}/channels/{channel}/playlists')
            new_playlists = os.listdir(
                f'{FOLDER_UPDATES}/{self.new_version}/channels/{channel}/playlists')
            common_playlists, old_playlists, new_playlists = make_summary(
                old_L=old_playlists, new_L=new_playlists, print_of=False)

            # Remove .csv
            common_playlists = list(map(lambda element: element.replace(
                '.csv', ''), common_playlists))
            old_playlists = list(map(lambda element: element.replace(
                '.csv', ''), old_playlists))
            new_playlists = list(map(lambda element: element.replace(
                '.csv', ''), new_playlists))

            self.summary['common_channels'][channel]['common_playlists'] = common_playlists
            self.summary['common_channels'][channel]['old_playlists'] = old_playlists
            self.summary['common_channels'][channel]['new_playlists'] = new_playlists

    def compare_common_playlist_items(self):
        for channel in self.summary['common_channels']:
            list_common_playlists = self.summary['common_channels'][channel]['common_playlists']
            self.summary['common_channels'][channel]['common_playlists'] = {}
            for playlist in list_common_playlists:
                self.summary['common_channels'][channel]['common_playlists'][playlist] = {
                }
                df_old_playlist = pd.read_csv(
                    f'./{FOLDER_UPDATES}/{self.old_version}/channels/{channel}/playlists/{playlist}.csv')
                df_new_playlist = pd.read_csv(
                    f'./{FOLDER_UPDATES}/{self.new_version}/channels/{channel}/playlists/{playlist}.csv')
                common_items, old_items, new_items = make_summary(
                    old_L=list(df_old_playlist.title), new_L=list(df_new_playlist.title), print_of=False)

                # Store the common items
                df_old_items = df_old_playlist[df_old_playlist['title'].isin(
                    old_items)] if old_items else pd.DataFrame()
                df_new_items = df_new_playlist[df_new_playlist['title'].isin(
                    new_items)] if new_items else pd.DataFrame()

                # self.summary['common_channels'][channel]['common_playlists'][playlist]['common_items'] = common_items
                self.summary['common_channels'][channel]['common_playlists'][playlist]['old_items'] = df_old_items.T.to_dict()
                self.summary['common_channels'][channel]['common_playlists'][playlist]['new_items'] = df_new_items.T.to_dict()


def run_comparison_workflow():
    now = datetime.now()

    print('\n')
    # Save for the first time
    if not os.path.isfile(f'{FOLDER_UPDATES}/versions.txt'):
        print('Download the data for the first time')
        save_data(time=now, first_time=True)
        now = datetime.now()

    # Save regularly
    with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f:
        print('Download the latest version of the data')
        old_time = f.read().split('\n')[0]
    save_data(time=now, first_time=False)

    # Compare everything
    print('Compare the two versions')
    CompareVersions(old_version=old_time,
                    new_version=now)
