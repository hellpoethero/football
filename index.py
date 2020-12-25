import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
dt = pd.read_csv("https://raw.githubusercontent.com/hellpoethero/football/main/big5.csv", index_col=0)


@app.route('/players')
def index(name=None):
    return "OK"


@app.route('/players')
def players(name=None):
    dt_table = dt[dt.columns[0:5]].copy()
    dt_table['url'] = dt_table.index
    dt_table['url'] = dt_table['url'].apply(lambda x: '<a href="/chart?player_id={0}">View</a>'.format(str(x)))

    return render_template('index.html', name=name, tables=[dt_table.to_html(escape=False, classes="table")])


@app.route('/chart')
def hello(name=None):
    return render_template('Polar Area Chart.html', name=name)


@app.route('/data')
def get_data():
    player_id = request.args.get('player_id')
    if player_id:
        player_json = json.loads(dt.iloc[int(player_id)].to_json())
        max_json = json.loads(dt[dt["minutes_90s"] >= 5].max().to_json())
        return {
            "player": player_json,
            "max": max_json
        }
    else:
        return "Fail"


@app.route('/search')
def search():
    player_name = request.args.get('name')
    if player_name:
        dt[dt["player"].str.contains(player_name)][dt.columns[0:5]].to_json(orient='records')
        return "OK"
    else:
        return "Fail"
