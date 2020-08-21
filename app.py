import os
import json

from flask import Flask, render_template

from models import Logs, LatestData

app = Flask(__name__)


@app.route('/')
def index():
    latest_data = LatestData()

    # For now one channel
    channel = latest_data.channels[0]

    return render_template('index.html', **locals())


@app.route('/logs')
def index_show_logs():

    # Get the logs from the files
    logs = Logs()

    return render_template('logs.html', **locals())


if __name__ == __name__:
    app.run()
