import shutil
import json
import os


from flask import Flask, render_template, request, redirect, flash

from config import *
from models import LogsByUpdate, LatestData, SavedChannels
from run import run_flow
from data_management import add_new_channel, initialize_folders, save_new_client_secrets, remove_files_empty_logs

app = Flask(__name__, static_url_path='/static/')

app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        run_flow()

        flash('You have just run the new update successfully!', 'success')
        return redirect('/logs')

    elif request.method == 'GET':
        latest_data = LatestData()

        return render_template('index.html', **locals())


@app.route('/logs')
def index_show_logs():

    if os.path.isfile(f'{FOLDER_UPDATES}/versions.txt'):
        with open(f'{FOLDER_UPDATES}/versions.txt', 'r') as f:
            latest_update = f.read().replace('\n', '')

    # Get the logs from the files
    logs_by_update = LogsByUpdate()

    return render_template('logs.html', **locals())


@app.route('/logs/remove_empty_updates', methods=['POST'])
def remove_empty_updates():
    remove_files_empty_logs()

    flash('You have successfully removed all the update times with empty logs!', 'deletion')
    return redirect('/logs')


@app.route('/logs/remove_log/<log_time>', methods=['POST'])
def remove_log(log_time):
    os.remove(f'{FOLDER_LOGS}/{log_time}.json')

    flash(
        f'You have successfully removed the update time: {log_time}', 'deletion')
    return redirect('/logs')


@app.route('/channels')
def index_channels():

    dict_channels = SavedChannels()

    return render_template('channels/index.html', **locals())


@app.route('/channels/delete/<channel_id>', methods=['POST'])
def unfollow_channel(channel_id):

    # Remove the channel
    shutil.rmtree(f'{FOLDER_CHANNELS}/{channel_id}')

    flash(
        f'You have successfully unfollowed the channel: {channel_id}', 'deletion')
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
    # # Old channel credentials
    if 'channelChoice' in request.form:
        add_new_channel(mine=True,
                        new_client_secrets=False,
                        channel_id_secrets=request.form['channelChoice']
                        )

        flash('You have just created a new channel', 'success')
        return redirect('/channels')

    # New credentials
    elif 'credentialsFile' in request.files:
        f = request.files['credentialsFile']

        if not f.filename:
            # TODO Put a flash because uploaded file

            flash('You need to upload a file', 'error')
            return redirect('/channels/new/new_credentials')

        else:
            #  Save the file
            file_name = 'client_secrets.json'
            f.save(f'{FOLDER_CHANNELS}/new_channel/client_secrets.json')

            # Add new channel
            add_new_channel(mine=True,
                            new_client_secrets=True,
                            )

            flash('You have just created a new channel', 'success')
            return redirect('/channels')


if __name__ == __name__:

    initialize_folders()
    app.run(debug=True, host='5000')
