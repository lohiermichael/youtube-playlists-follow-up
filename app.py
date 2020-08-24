import os
import json

from flask import Flask, render_template, request, redirect

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


if __name__ == __name__:
    app.run()
