# Video Tutorial: https://www.youtube.com/watch?v=th5_9woFJmk

import os
from googleapiclient.discovery import build

api_key = os.environ['PROJECT_API_KEY']
print(api_key)

youtube = build(serviceName='youtube',
                version='v3',
                developerKey=api_key)

request = youtube.channels().list(
    forUsername='jemapellemichael',
    part='statistics'
)

response = request.execute()

print(response)
