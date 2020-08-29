import os
import json
import shutil

from flask import Flask, render_template, request, redirect

from config import FOLDER_CHANNELS
from models import LogsByUpdate, LatestData, SavedChannels
from run import run_flow
from data_management import add_new_channel, initialize_folders

app = Flask(__name__, static_url_path='/static/')


@app.route('/', methods=['GET', 'POST'])
def index():
    initialize_folders()

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

    dict_channels = SavedChannels()

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

    dict_channels = SavedChannels()

    return render_template('channels/new/old_channel_credentials.html', **locals())


@app.route('/channels/create', methods=['POST'])
def create_channel():

    add_new_channel(mine=True,
                    new_client_secrets=False,
                    channel_id_secrets=request.form['channelChoice']
                    )

    return redirect('/channels')


if __name__ == __name__:

    initialize_folders()
    app.run()
