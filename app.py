import os
import json
import shutil

from flask import Flask, render_template, request, redirect

from config import FOLDER_CHANNELS
from models import LogsByUpdate, LatestData
from run import run_flow

app = Flask(__name__, static_url_path='/static/')


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        run_flow()

        return redirect('/logs')

    elif request.method == 'GET':
        latest_data = LatestData()

        return render_template('index.html', **locals())


@app.route('/logs')
def index_show_logs():

    # Get the logs from the files
    logs_by_update = LogsByUpdate()

    return render_template('logs.html', **locals())


@app.route('/channels')
def index_channels():

    channel_ids = [channel_id for channel_id in next(
        os.walk(FOLDER_CHANNELS))[1] if channel_id != 'new_channel']

    with open(f'{FOLDER_CHANNELS}/history_channels.json', 'r') as f:
        history_channels = json.load(f)

    dict_channels = {
        channel_id: history_channels[channel_id] for channel_id in channel_ids}

    return render_template('channels/index.html', **locals())


@app.route('/channels/delete/<channel_id>', methods=['POST'])
def unfollow_channel(channel_id):

    # Remove the channel
    shutil.rmtree(f'{FOLDER_CHANNELS}/{channel_id}')
    print(f'Channel {channel_id} removed!')

    return redirect('/channels')


@app.route('/channels/new/strategy_choice')
def choose_strategy():
    return render_template('channels/new/strategy_choice.html')


@app.route('/channels/new/new_credentials')
def new_credentials():
    return render_template('channels/new/new_credentials.html')


@app.route('/channels/new/old_channel_credentials')
def old_credentials():
    return render_template('channels/new/old_channel_credentials.html')


if __name__ == __name__:
    app.run()
