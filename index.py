import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import json

app = Flask(__name__)
dt = pd.read_csv("https://raw.githubusercontent.com/hellpoethero/football/main/big5.csv", index_col=0)
# dt = pd.read_csv("big5.csv", index_col=0)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/players')
def players(name=None):
    dt_table = dt[dt.columns[0:9]].copy()
    dt_table['url'] = dt_table.index
    dt_table['url'] = dt_table['url'].apply(lambda x: '<a href="/chart?player_id={0}">View</a>'.format(str(x)))

    return render_template('players.html', tables=[dt_table.to_html(escape=False, classes="table")])


@app.route('/chart')
def chart(name=None):
    return render_template('Polar Area Chart.html', name=name)


@app.route('/data', methods=["GET"])
def get_data():
    player_id = request.args.get('player_id')
    position = request.args.get('position')
    min_90s = 5
    if player_id:
        dt_copy = dt.copy()
        dt_copy["index"] = dt_copy.index

        ids = player_id.split(",")
        player_data = dt_copy.loc[int(ids[0])]
        compare_data = player_data
        if len(ids) > 1:
            compare_data = dt_copy.loc[int(ids[1])]

        if position:
            dt_copy = dt_copy[(dt_copy["position"].str.lower().str.contains(position.lower())) |
                              (dt_copy["index"] == player_data["index"]) |
                              (dt_copy["index"] == compare_data["index"])]

        if (player_data["minutes_90s"] >= min_90s) and (compare_data["minutes_90s"] >= min_90s):
            dt_copy = dt_copy[dt_copy["minutes_90s"] >= min_90s]
        for col in dt.columns[8:]:
            dt_copy[col+"_rank"] = np.around((dt_copy[col]).rank(pct=True, na_option='bottom', method='min') * 100)

        player_data = dt_copy.loc[int(ids[0])]
        player_json = json.loads(player_data.to_json())
        response = {
            "success": 1,
            "player": player_json
        }
        if len(ids) > 1:
            compare_data = dt_copy.loc[int(ids[1])]
            compare_json = json.loads(compare_data.to_json())
            response["compare"] = compare_json

        max_json = json.loads(dt_copy.max().to_json())
        response["max"] = max_json
        return response
    else:
        return {
            "success": 0
        }


@app.route('/search')
def search():
    player_name = request.args.get('name')
    if player_name:
        dt['index'] = dt.index
        cols = ['index','player','nationality','position','squad','age']
        response = dt[dt["player"].str.lower().str.contains(player_name.lower())][cols].to_json(orient='records')
        return response
    else:
        return "Fail"
