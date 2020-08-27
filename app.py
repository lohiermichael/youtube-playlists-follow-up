import os
import json

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


@app.route('/channels', methods=['GET', 'DELETE'])
def index_channels():
    if request.method == 'GET':

        channel_ids = [channel_id for channel_id in next(
            os.walk(FOLDER_CHANNELS))[1] if channel_id != 'new_channel']

        with open(f'{FOLDER_CHANNELS}/history_channels.json', 'r') as f:
            history_channels = json.load(f)

        dict_channels = {
            channel_id: history_channels[channel_id] for channel_id in channel_ids}

        return render_template('channels/index.html', **locals())

    elif request.method == 'POST':
        return redirect('channels/index.html')


if __name__ == __name__:
    app.run()
