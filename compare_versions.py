import os
import shutil
import json
from typing import Tuple

from datetime import datetime
from time import sleep
import pandas as pd

from save_data import save_data


def make_summary(old_L: list, recent_L: list, print_of: bool = True) -> Tuple[list]:
    common_elements = [element for element in old_L if element in recent_L]
    elements_old_only = [
        element for element in old_L if element not in recent_L]
    elements_recent_only = [
        element for element in recent_L if element not in old_L]

    # Summary
    if print_of:
        print(f'In common: {len(common_elements)}')
        print(common_elements)
        print('\n')
        print(f'In old and not in recent: {len(elements_old_only)}')
        print(elements_old_only)
        print('\n')
        print(f'In recent and not in old: {len(elements_recent_only)}')
        print(elements_recent_only)
        print('\n')

    return common_elements, elements_old_only, elements_recent_only


class CompareVersions:
    def __init__(self, old_version, recent_version):
        self.old_version = old_version
        self.recent_version = recent_version
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
        self.compare_playlist_items()
        self._save_comparison_results()

    def _save_comparison_results(self):
        with open('comparison_results.json', 'w') as f:
            json.dump(self.summary, f)

    def compare_channels(self):
        old_channels = os.listdir(self.old_version)
        recent_channels = os.listdir(self.recent_version)
        self.summary['common_channels'], self.summary['old_channels'], self.summary['new_channels'] = make_summary(
            old_L=old_channels, recent_L=recent_channels, print_of=False)

    def compare_playlists(self):
        # Store elements new channels
        # self.store_elements_channels(self, type_channel='old_channels') TODO

        # Playlists in common
        self.compare_common_playlists()

        # Store old channels

    def compare_common_playlists(self):

        list_common_channels = self.summary['common_channels']
        self.summary['common_channels'] = {}

        for channel in list_common_channels:
            self.summary['common_channels'][channel] = {}
            old_playlists = os.listdir(f'{self.old_version}/{channel}')
            recent_playlists = os.listdir(f'{self.recent_version}/{channel}')
            common_playlists, old_playlists, new_playlists = make_summary(
                old_L=old_playlists, recent_L=recent_playlists, print_of=False)

            # Remove .csv
            common_playlists = list(map(lambda element: element.replace(
                '.csv', ''), common_playlists))
            old_playlists = list(map(lambda element: element.replace(
                '.csv', ''), old_playlists))
            recent_playlists = list(map(lambda element: element.replace(
                '.csv', ''), recent_playlists))

            # Remove playlist
            common_playlists.remove('playlists')

            self.summary['common_channels'][channel]['common_playlists'] = common_playlists
            self.summary['common_channels'][channel]['old_playlists'] = old_playlists
            self.summary['common_channels'][channel]['new_playlists'] = new_playlists

    def compare_playlist_items(self):
        # Store old playlists

        # Playlists in common
        self.compare_common_playlist_items()

        # Store new playlists

    def compare_common_playlist_items(self):
        for channel in self.summary['common_channels']:
            list_common_playlists = self.summary['common_channels'][channel]['common_playlists']
            self.summary['common_channels'][channel]['common_playlists'] = {}
            for playlist in list_common_playlists:
                self.summary['common_channels'][channel]['common_playlists'][playlist] = {
                }
                df_old_playlist = pd.read_csv(
                    f'./{self.old_version}/{channel}/{playlist}.csv')
                df_recent_playlist = pd.read_csv(
                    f'./{self.recent_version}/{channel}/{playlist}.csv')
                common_items, old_items, new_items = make_summary(
                    old_L=list(df_old_playlist.title), recent_L=list(df_recent_playlist.title), print_of=False)
                self.summary['common_channels'][channel]['common_playlists'][playlist]['common_items'] = common_items
                self.summary['common_channels'][channel]['common_playlists'][playlist]['old_items'] = old_items
                self.summary['common_channels'][channel]['common_playlists'][playlist]['new_items'] = new_items


if __name__ == "__main__":
    now = datetime.now()
    # Run first time
    if not os.path.isfile('./versions.txt'):
        print('Download the data for the first time')
        save_data(time=now, first_time=True)
        now = datetime.now()

    with open('versions.txt', 'r') as f:
        print('Download the most recent version of the data')
        old_time = f.read().split('\n')[0]
    save_data(time=now, first_time=False)

    # Compare everything
    try:
        print('compare the two versions')
        summary_comparison = CompareVersions(
            old_version=f'{old_time}', recent_version=f'{now}').summary

        # Analyze summary comparison

        # Clean date for next time
        with open('versions.txt', 'r') as f_in:
            data = f_in.read().splitlines(True)
        with open('versions.txt', 'w') as f_out:
            f_out.writelines(data[1:])

        # Remove old data
        shutil.rmtree(f'./{old_time}/')

    except Exception as e:
        print(e)
        shutil.rmtree(f'./{old_time}/')
        shutil.rmtree(f'./{now}/')
        os.remove('versions.txt')
