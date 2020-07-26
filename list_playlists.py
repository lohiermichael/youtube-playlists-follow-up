from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import re
load_dotenv()


def get_list_playlists(user_name: str) -> list:
    """Get the names of the playlists of a user

    Args:
        user_name (str): The Youtube username

    Returns:
        list: The list of the playlists names of the user 
    """

    data = requests.get(f'http://www.youtube.com/{user_name}/playlists')

    # Load data into bs4
    soup = BeautifulSoup(data.text, 'html.parser')

    # Get playlists names: They are in script
    script_str = str(soup.find_all('script'))
    # In text
    txts = re.compile('"text":"[a-zA-Z\s]*"')

    # Build first
    playlists_names = [occ.group() for occ in txts.finditer(script_str)]

    # Remove "text"
    playlists_names = [element[7:].replace('"', '')
                       for element in playlists_names]

    # Remove undesired elements
    undesired = {' video', 'Putar semua',
                 'Sedang diputar', 'Lihat playlist lengkap', 'Telusuri'}
    playlists_names = list(
        filter(lambda element: element not in undesired, playlists_names))

    # When Youtube is present no need to keep onwards names
    for i, name in enumerate(playlists_names):
        if 'YouTube' in name:
            playlists_names = playlists_names[:i]

    # Sort playlists_names
    playlists_names.sort()

    return playlists_names


if __name__ == "__main__":
    # Environment variables
    USER_NAME = os.getenv('USER_NAME')

    playlists_names = get_list_playlists(user_name=USER_NAME)
    print(playlists_names)
