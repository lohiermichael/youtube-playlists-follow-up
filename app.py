import os
import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open('versions.txt', 'r') as f:
        latest_update = f.read()
    return render_template('index.html', **locals())


@app.route('/logs/index')
def index_logs():
    logs_update_times = [logs_update_time.replace(
        '.json', '') for logs_update_time in os.listdir('logs/')]

    return render_template('logs/index.html', **locals())


@app.route('/logs/show/<logs_update_time>')
def show_logs(logs_update_time):

    with open(f'./logs/{logs_update_time}.json') as f:
        dict_logs = json.load(f)

    previous_update_time = dict_logs['previous_update_time']
    logs = dict_logs['logs']

    return render_template('logs/show.html', **locals())


if __name__ == __name__:
    app.run()
