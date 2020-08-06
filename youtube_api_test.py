import os
import pandas as pd

from youtube_api import YouTubeDataAPI

api_key = os.environ['YOUTUBE_DATA_API_KEY']
yt = YouTubeDataAPI(api_key)
searches = yt.search('alexandria', max_results=5)
df_searches = pd.DataFrame(searches)
df_searches.to_csv('videos_search.csv')
