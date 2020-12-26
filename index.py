import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
dt = pd.read_csv("https://raw.githubusercontent.com/hellpoethero/football/main/big5.csv", index_col=0)


@app.route('/')
def index(name=None):
    dt_table = dt[dt.columns[0:9]].copy()
    dt_table['url'] = dt_table.index
    dt_table['url'] = dt_table['url'].apply(lambda x: '<a href="/chart?player_id={0}">View</a>'.format(str(x)))

    return render_template('index.html', name=name, tables=[dt_table.to_html(escape=False, classes="table")])


@app.route('/chart')
def hello(name=None):
    return render_template('Polar Area Chart.html', name=name)


@app.route('/data', methods=["GET"])
def get_data():
    player_id = request.args.get('player_id')
    if player_id:
        ids = player_id.split(",")
        player_json = json.loads(dt.iloc[int(ids[0])].to_json())
        max_json = json.loads(dt[dt["minutes_90s"] >= 5].max().to_json())
        response = {
            "player": player_json,
            "max": max_json
        }
        if len(ids) > 1:
            compare_json = json.loads(dt.iloc[int(ids[1])].to_json())
            response["compare"] = compare_json
        return response
    else:
        return "Fail"


@app.route('/search')
def search():
    player_name = request.args.get('name')
    if player_name:
        dt['index'] = dt.index
        cols = ['index','player','nationality','position','squad','age']
        response = dt[dt["player"].str.lower().str.contains(player_name)][cols].to_json(orient='records')
        return response
    else:
        return "Fail"
