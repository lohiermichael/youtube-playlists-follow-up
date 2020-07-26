from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Environment variables
load_dotenv()
USER_NAME = os.getenv('USER_NAME')
print(USER_NAME)

# Get the data
data = requests.get(f'http://www.youtube.com/{USER_NAME}')

# Load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')
print(soup)
