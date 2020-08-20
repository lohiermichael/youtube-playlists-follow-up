from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    with open('versions.txt', 'r') as f:
        latest_update = f.read()
    return render_template('index.html', latest_update=latest_update)


@app.route('/logs/index')
def index_logs():
    logs_update_times = [logs_update_time.replace(
        '.json', '') for logs_update_time in os.listdir('logs/')]

    return render_template('logs/index.html', logs_update_times=logs_update_times)


@app.route('/logs/show/<logs_update_time>')
def show_logs(logs_update_time):
    logs_update_time = logs_update_time.replace('%', ' ')
    logs_update_time = logs_update_time.replace('%20', ' ')
    return render_template('logs/show.html', logs_update_time=logs_update_time)


if __name__ == __name__:
    app.run()
