import pandas as pd
import json
# import json_tools
from time import time
from flask import g, jsonify, request, Response, make_response
import psycopg2
from flask_cors import cross_origin

# from main import TaskVisAPIs, tasks,NLPapi
# from NLI.helpers import get_attributemap_for_NLP
from visrec.src.main import TaskVisAPIs
# from HtmlOut import HTML_Out2, HTML_Out
from visrec.src import app

@app.route('/api/viss', methods=['GET'])
@cross_origin()
def get_test():
    id = request.args.get('id')
    return id

@app.route('/api/columns', methods=['GET'])
@cross_origin()
def get_columns():
    # j = request.get_json()
    # dataset=j['dataset']
    dataset = request.args.get('dataset')
    columns=None
    if dataset=='cars':
        columns=[
        {"field": "Name", "type": "nominal"},
        {"field": "Miles_per_Gallon", "type": "quantitative"},
        {"field": "Horsepower", "type": "quantitative"},
        {'field': 'Weight_in_lbs', 'type': 'quantitative'},
        {'field': 'Acceleration', 'type': 'quantitative'},
        {'field': 'Year', 'type': 'temporal'},
        {'field': 'Origin', 'type': 'nominal'},
        {"field": "Cylinders", "type": "ordinal"},
        {"field": "Displacement", "type": "quantitative"},
    ]
    elif dataset=="covid": 
        columns=[
        {'field': 'Lat', 'type': 'quantitative'},
        {'field': 'Long', 'type': 'quantitative'},
        {'field': 'month', 'type': 'ordinal'},
        {'field': 'State', 'type': 'nominal'},
        {'field': 'region', 'type': 'nominal'},
        {'field': 'USMapID', 'type': 'nominal'},
        {'field': 'death', 'type': 'quantitative'},
        {'field': 'confirmed', 'type': 'quantitative'},
        {'field': 'Population', 'type': 'quantitative'},
        {'field': 'date', 'type': 'temporal'}
    ]
    elif dataset=="weather": 
        columns=[
        {"field": "date", "type": "temporal"},
        {"field": "precipitation", "type": "quantitative"},
        {"field": "temp_max", "type": "quantitative"},
        {"field": "temp_min", "type": "quantitative"},
        {"field": "location", "type": "nominal"},
        {"field": "wind", "type": "quantitative"},
        {"field": "weather", "type": "nominal"},
    ]
    elif dataset=="AirpotDeley": 
        columns=[
        {"field": "date", "type": "temporal"},
        {"field": "depdelay", "type": "quantitative"},
        {"field": "arrdelay", "type": "quantitative"},
        {"field": "time", "type": "quantitative"},
        {"field": "carrier", "type": "nominal"},
        {"field": "destcity", "type": "nominal"},
    ]
    elif dataset=="driving": 
        columns=[
        {"field": "year", "type": "temporal"},
        {"field": "miles", "type": "quantitative"},
        {"field": "gas", "type": "quantitative"},
        {"field": "side", "type": "nominal"},
    ]
    elif dataset=="HappinessRanking": 
        columns=[
        {"field": "Time", "type": "temporal"},
        {"field": "Region", "type": "nominal"},
        {"field": "Country", "type": "nominal"},
        {"field": "Happiness Score", "type": "quantitative"},
        {"field": "Happiness Rank", "type": "quantitative"},
        {"field": "Family", "type": "quantitative"},
        {"field": "Health", "type": "quantitative"},
        {"field": "Freedom", "type": "quantitative"},
        {"field": "Trust", "type": "quantitative"},
        {"field": "Economy", "type": "quantitative"},
        {"field": "Generosity", "type": "quantitative"},
        {"field": "Dystopia Residual", "type": "quantitative"},
    ]
    elif dataset=="HollywoodsStories": 
        columns=[
        {"field": "Year", "type": "temporal"},
        {"field": "Film", "type": "nominal"},
        {"field": "Genre", "type": "nominal"},
        {"field": "Lead Studio", "type": "nominal"},
        {"field": "Audience score", "type": "quantitative"},
        {"field": "Profitability", "type": "quantitative"},
        {"field": "Rotten Tomatoes", "type": "quantitative"},
        {"field": "Worldwide Gross", "type": "quantitative"},
    ]
    elif dataset=="movies": 
        columns=[
        {"field": "Release_Date", "type": "temporal"},
        {"field": "Title", "type": "nominal"},
        {"field": "MPAA_Rating", "type": "nominal"},
        {"field": "Distributor", "type": "nominal"},
        {"field": "Source", "type": "nominal"},
        {"field": "Major_Genre", "type": "nominal"},
        {"field": "Creative_Type", "type": "nominal"},
        {"field": "Director", "type": "nominal"},
        {"field": "US_Gross", "type": "quantitative"},
        {"field": "Worldwide_Gross", "type": "quantitative"},
        {"field": "US_DVD_Sales", "type": "quantitative"},
        {"field": "Production_Budget", "type": "quantitative"},
        {"field": "Running_Time_min", "type": "quantitative"},
        {"field": "Rotten_Tomatoes_Rating", "type": "quantitative"},
        {"field": "IMDB_Rating", "type": "quantitative"},
        {"field": "IMDB_Votes", "type": "quantitative"},
    ]
    jsdata = json.dumps(columns)
    return Response(jsdata, mimetype='application/json')


@app.route('/api/Reco', methods=['POST'])
@cross_origin()
def Recommendation():
    j = request.get_json()
    Dataset=j['dataset']
    ColumnTypes=j['ColumnTypes']
    task=j['task']
    mode=j['mode']
    url = './visrec/dataset/{}.json'.format(Dataset)
    with open(url, 'r', encoding='UTF-8') as f:
        DataJson = json.load(f)
    # print("Dataset",Dataset)
    # print("ColumnTypes",ColumnTypes)
    # print("task",task)
    # print("mode",mode)
    # print("-------------------------------------")
    Recos, Data = TaskVisAPIs(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0, mode=mode)
    result={
        "Data":Data,
        "Recos":Recos
    }
    # Recos["data"]=Data
    # print(Recos)
    return jsonify(result)

# def test()
# TaskVisAPIs(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0, mode=1)


'''-----------Columns and corresponding type of example datasets-----------'''
###type:quantitative, ordinal, nominal, temporal###
# '''
DataColumnMap = {
    "cars": [
        # {"field": "Name", "type": "nominal"},
        # {"field": "Miles_per_Gallon", "type": "quantitative"},
        {"field": "Horsepower", "type": "quantitative"},
        # {'field': 'Weight_in_lbs', 'type': 'quantitative'},
        # {'field': 'Acceleration', 'type': 'quantitative'},
        {'field': 'Year', 'type': 'temporal'},
        {'field': 'Origin', 'type': 'nominal'},
        {"field": "Cylinders", "type": "ordinal"},
        {"field": "Displacement", "type": "quantitative"},
    ],
    "covid": [
        {'field': 'Lat', 'type': 'quantitative'},
        {'field': 'Long', 'type': 'quantitative'},
        # {'field': 'month', 'type': 'ordinal'},
        # {'field': 'State', 'type': 'nominal'},
        {'field': 'region', 'type': 'nominal'},
        {'field': 'USMapID', 'type': 'nominal'},
        {'field': 'death', 'type': 'quantitative'},
        {'field': 'confirmed', 'type': 'quantitative'},
        # {'field': 'Population', 'type': 'quantitative'},
        {'field': 'date', 'type': 'temporal'}
    ],
    "weather": [
        {"field": "date", "type": "temporal"},
        {"field": "precipitation", "type": "quantitative"},
        {"field": "temp_max", "type": "quantitative"},
        {"field": "temp_min", "type": "quantitative"},
        {"field": "location", "type": "nominal"},
        {"field": "wind", "type": "quantitative"},
        {"field": "weather", "type": "nominal"},
    ],
    "AirpotDeley": [
        {"field": "date", "type": "temporal"},
        {"field": "depdelay", "type": "quantitative"},
        {"field": "arrdelay", "type": "quantitative"},
        {"field": "time", "type": "quantitative"},
        {"field": "carrier", "type": "nominal"},
        {"field": "destcity", "type": "nominal"},
    ],
    "driving": [
        {"field": "year", "type": "temporal"},
        {"field": "miles", "type": "quantitative"},
        {"field": "gas", "type": "quantitative"},
        {"field": "side", "type": "nominal"},
    ],
    "HappinessRanking": [
        {"field": "Time", "type": "temporal"},
        {"field": "Region", "type": "nominal"},
        # {"field": "Country", "type": "nominal"},
        {"field": "Happiness Score", "type": "quantitative"},
        # {"field": "Happiness Rank", "type": "quantitative"},
        # {"field": "Family", "type": "quantitative"},
        {"field": "Health", "type": "quantitative"},
        {"field": "Freedom", "type": "quantitative"},
        {"field": "Trust", "type": "quantitative"},
        {"field": "Economy", "type": "quantitative"},
        # {"field": "Generosity", "type": "quantitative"},
        # {"field": "Dystopia Residual", "type": "quantitative"},
    ],
    "HollywoodsStories": [
        {"field": "Year", "type": "temporal"},
        {"field": "Film", "type": "nominal"},
        {"field": "Genre", "type": "nominal"},
        {"field": "Lead Studio", "type": "nominal"},
        {"field": "Audience score", "type": "quantitative"},
        {"field": "Profitability", "type": "quantitative"},
        # {"field": "Rotten Tomatoes", "type": "quantitative"},
        # {"field": "Worldwide Gross", "type": "quantitative"},
    ],
    "movies": [
        {"field": "Release_Date", "type": "temporal"},
        {"field": "Title", "type": "nominal"},
        # {"field": "MPAA_Rating", "type": "nominal"},
        {"field": "Distributor", "type": "nominal"},
        # {"field": "Source", "type": "nominal"},
        {"field": "Major_Genre", "type": "nominal"},
        {"field": "Creative_Type", "type": "nominal"},
        {"field": "Director", "type": "nominal"},
        # {"field": "US_Gross", "type": "quantitative"},
        # {"field": "Worldwide_Gross", "type": "quantitative"},
        {"field": "US_DVD_Sales", "type": "quantitative"},
        {"field": "Production_Budget", "type": "quantitative"},
        # {"field": "Running_Time_min", "type": "quantitative"},
        # {"field": "Rotten_Tomatoes_Rating", "type": "quantitative"},
        {"field": "IMDB_Rating", "type": "quantitative"},
        {"field": "IMDB_Votes", "type": "quantitative"},
    ]
}
# '''

