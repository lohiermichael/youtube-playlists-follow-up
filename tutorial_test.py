# Video Tutorial: https://www.youtube.com/watch?v=th5_9woFJmk

import os
from googleapiclient.discovery import build

api_key = os.environ['PROJECT_API_KEY']

youtube = build(serviceName='youtube',
                version='v3',
                developerKey=api_key)

request = youtube.channels().list(
    forUsername=os.environ['YOUTUBE_USERNAME'],
    part='statistics'
)

response = request.execute()
for channel in response['items']:

print(response)
