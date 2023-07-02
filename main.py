import os
from flask import Flask, render_template, jsonify
import requests
from flatten_json import flatten

app = Flask(__name__)

url = 'https://badimo.nyc3.digitaloceanspaces.com/crew_leaderboard/snapshot/top/50/season/3/latest.json'

@app.route('/')
def index():
    return render_template('tabledata.html')

@app.route('/table-data')
def table_data():
    response = requests.get(url)
    data = response.json()

    flattened_data = [flatten(item) for item in data]

    if flattened_data:
        keys = list(flattened_data[0].keys())
        table = [[item.get(key, "") for key in keys] for item in flattened_data]
    else:
        keys = []
        table = []

    # Replace column names
    keys = [key.replace("Member UserID", "Member").replace("User ID", "User ID") for key in keys]

    return {"table": table, "headers": keys}

@app.route('/graph')
def graph():
    return render_template('livegraph.html')

@app.route('/graph-data')
def graph_data():
    response = requests.get(url)
    data = response.json()

    timestamps = []
    crew_count = []

    for item in data:
        timestamps.append(item['TimeStamp'])
        crew_count.append(item['Crew Count'])

    return jsonify({"x": timestamps, "y": crew_count})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

