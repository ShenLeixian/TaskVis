import pandas as pd
import json
# import json_tools
from time import time
from flask import g, jsonify, request, Response, make_response
import psycopg2

# from main import TaskVisAPIs, tasks,NLPapi
# from NLI.helpers import get_attributemap_for_NLP
from visrec.src.main import TaskVisAPIs
# from HtmlOut import HTML_Out2, HTML_Out
from visrec.src import app

@app.route('/api/viss', methods=['GET'])
def get_test():
    id = request.args.get('id')
    return id

@app.route('/api/columns', methods=['GET'])
def get_columns():
    # j = request.get_json()
    # dataset=j['dataset']
    dataset = request.args.get('dataset')
    columns=[]
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
    ],
    elif dataset=="weather": 
        columns=[
        {"field": "date", "type": "temporal"},
        {"field": "precipitation", "type": "quantitative"},
        {"field": "temp_max", "type": "quantitative"},
        {"field": "temp_min", "type": "quantitative"},
        {"field": "location", "type": "nominal"},
        {"field": "wind", "type": "quantitative"},
        {"field": "weather", "type": "nominal"},
    ],
    elif dataset=="AirpotDeley": 
        columns=[
        {"field": "date", "type": "temporal"},
        {"field": "depdelay", "type": "quantitative"},
        {"field": "arrdelay", "type": "quantitative"},
        {"field": "time", "type": "quantitative"},
        {"field": "carrier", "type": "nominal"},
        {"field": "destcity", "type": "nominal"},
    ],
    elif dataset=="driving": 
        columns=[
        {"field": "year", "type": "temporal"},
        {"field": "miles", "type": "quantitative"},
        {"field": "gas", "type": "quantitative"},
        {"field": "side", "type": "nominal"},
    ],
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
    ],
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
    ],
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
    return jsonify(columns)

@app.route('/api/Reco', methods=['POST'])
def Recommendation():
    j = request.get_json()
    Dataset=j['dataset']
    ColumnTypes=j['ColumnTypes'][0]
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
    # print(Recos)
    return jsonify(Recos)

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

'''------------------input dataset (Necessary)--------------------
You can choose between json and csv formats to enter your own data. The examples provided in this project are all json.
To use examples, you can choose one of the following dataset name for variable Dataset.
['cars', 'covid', 'weather', 'AirpotDeley', 'driving', 'HappinessRanking', 'HollywoodsStories', 'movies']

# input json dataset name
Dataset = "cars"
url = './dataset/{}.json'.format(Dataset)
with open(url, 'r', encoding='UTF-8') as f:
    DataJson = json.load(f)
# DataCsv=pd.read_csv("../dataset/movies.csv")
# input csv dataset local address
# url=""
# DataPd = pd.read_csv(url,encoding='utf-8')
'''

'''------------------input ColumnTypes (Optional)--------------------
ColumnTypes get columns and corresponding type of the dataset from DataColumnMap.
You can modify it in the DataColumnMap and select all the columns or some columns of interest. 
ColumnTypes allow three input modes:
(1) ColumnTypes=[], which means no columns of interest and the column type will be automatically determined by the system.
(2) ColumnTypes=[
        {"field": "Horsepower"},
        {'field': 'Year'},
        {'field': 'Origin'},
        {"field": "Cylinders"},
        {"field": "Displacement"},
    ], which means with columns of interest and the column type will be automatically determined by the system.
(3) ColumnTypes=[
        {"field": "Horsepower", "type": "quantitative"},
        {'field': 'Year', 'type': 'temporal'},
        {'field': 'Origin', 'type': 'nominal'},
        {"field": "Cylinders", "type": "ordinal"},
        {"field": "Displacement", "type": "quantitative"},
    ], which means with columns of interest and corresponding type.
We provide mode(3) for example datasets.

ColumnTypes = DataColumnMap[Dataset]
# ColumnTypes = []
'''

'''------------------input task (Optional)------------------
task available:
['change_over_time', 'characterize_distribution', 'cluster', 'comparison', 'compute_derived_value', 'correlate', 'determine_range', 
'deviation', 'error_range', 'find_anomalies', 'find_extremum', 'magnitude', 'part_to_whole', 'retrieve_value', 'sort', 'spatial', 'trend']
task allow three input modes:
(1) task=None, which means no task.
(2) task='characterize_distribution', which means with single task.
(3) tasklist=['characterize_distribution','find_extremum', 'magnitude'], which means with multiple tasks. Only allowed for API RecommendationWithMultiTask().

# task = 'change_over_time'
task=['characterize_distribution','find_extremum', 'magnitude']
'''

'''------------------APIs------------------
TaskVis supports 6 APIs:
mode 1:Individual recommendation with single task
mode 2:Individual recommendation with multiple tasks
mode 3:Individual recommendation without task
mode 4:Combination recommendation without task
mode 5:Combination recommendation with multiple tasks
mode 6:Combination recommendation with single task

parameter of function TaskVisAPIs:
Data: dataset to be analyzed
ColumnTypes: columns and corresponding type of the dataset
task: analysis task
Num: Get top Num charts
mode: APIs mode

time_s = time()
Recos, Data = TaskVisAPIs(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0, mode=2)
# print(Recos)
# Recos, Data,ColDic = NLPapi(Data=DataJson)
'''
# aa=get_attributemap_for_NLP(pd.DataFrame(DataJson))
# query="compare GDP in different province"
# print(NLPapi(aa,query))
# time_e = time()

# Generate html in ./html
# HTML_Out(Data=Data, Recos=Recos, ColumnTypes=ColDic, time=time_e - time_s)
















###*****************supplement******************###
# individual_recommendation
# for task in tasks:
#     time_s = time()
#     Recos,Data = TaskVisAPIs(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0,mode=1)
#     time_e = time()
#     if Recos is None:
#         continue
#     HTML_Out(Data=Data, Recos=Recos, task=task,ColumnTypes=ColumnTypes, time=time_e - time_s)

#-------------------------------------------------#

# combination_recommendation_without_task
# index=1
# for col in Cols:
#     time_s = time()
#     Recos = RecommendationCombinationnew(Data=DataJson, ColumnTypes=col)
#     time_e = time()
#     if Recos is None:
#         continue
#     HTML_Out(DataJson,Recos, index,col,time_e-time_s)
#     index+=1

#-------------------------------------------------#

# combination_recommendation_with_task
# for task in tasks:
#     time_s = time()
#     Recos = RecommendationCombination_SingleTask(Data=DataJson, ColumnTypes=ColumnTypes,task=task)
#     time_e = time()
#     if Recos is None:
#         continue
#     HTML_Out(DataJson,Recos, task,ColumnTypes,time_e-time_s)

###*****************supplement******************###

# 多task
# Recos_task = {}
# Times = {}
# ans=[]
# ind=279
# for task in tasks:
#     time_s = time()
#     Recos = RecommendationWithTask(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0)
#     time_e = time()
#     if Recos is None:
#         continue
#     DeRecos=[]
#     DeRecos.append(Recos[0])
#     ans.append(ind+0)
#     for i in range(len(Recos)):
#         for j in range(len(DeRecos)):
#             flag=1
#             comp=json_tools.diff(Recos[i].props,DeRecos[j].props)
#             if len(comp)<1:
#                 break
#             for item in comp:
#                 key=list(item.keys())[0]
#                 if key!="replace":
#                     flag=0
#                     break
#                 else:
#                     strs=item['replace'].split("/")
#                     # if not 'aggregate' in strs and not 'x' in strs and not 'y' in strs and not 'color' in strs and not 'size' in strs and not 'shape' in strs:
#                     if 'stack' in strs or 'mark' in strs:
#                         flag=0
#                         break
#             if flag:
#                 break
#             if j==len(DeRecos)-1:
#                 DeRecos.append(Recos[i])
#                 ans.append(ind+i)
#     ind+=len(Recos)
# print(ans)
# Recos_task[task] = DeRecos
# Times[task] = time_e - time_s
# HTML_Out2(DataJson, Recos_task,ColumnTypes,Times)


# from vega_datasets import data
# conn = psycopg2.connect(database="viznet", user="admin", password="9980206", host="127.0.0.1", port="5432")
# cur = conn.cursor()
# # Recos_task={}
# # Times={}
# for task in tasks:
#     time_s = time()
#     Recos = RecommendationWithTask(Data=DataJson, ColumnTypes=ColumnTypes, task=task, Num=0)
#     time_e = time()
#     if Recos==None:
#         continue
#     # Recos_task[task] = Recos
#     # Times[task] = time_e - time_s
#     index=0

#     for item in Recos:
#         # vegalite=item.props
#         # vegalite["data"]={"values":json.dumps(DataJson)}
#         # addr="D:\\Project\\viznet-master\\experiment\\system\\frontend\\src\\assets\\pic\\"+Dataset+"_"+str(task)+"_"+str(index)+".png"
#         # try:
#         #     chart=alt.Chart.from_dict(vegalite)
#         #     # chart.save(addr)
#         # except Exception as e:
#         #     print(addr)
#             # print("vegalite",vegalite)
#             # print("Exception",e)
#             # print('---------------')
#         sql='''INSERT INTO Visualization (dataset,task,innerid,vis,cost) \
#             VALUES ('{}', '{}', {}, '{}',{} )'''.format(Dataset,task,index,json.dumps(item.props),item.cost)
#         cur.execute(sql)
#         index+=1
# # HTML_Out2(DataJson, Recos_task,ColumnTypes,Times)
# conn.commit()
# conn.close()


# 多task输出html
# for col in Cols2:
#     Recos_task = {}
#     Times = {}
#     for task in tasks:
#         # print(task)
#         time_s = time()
#         Recos = RecommendationWithTask(Data=DataJson, ColumnTypes=col, task=task, Num=0)
#         time_e = time()
#         Recos_task[task] = Recos
#         Times[task] = time_e - time_s
#         # print("Time last %f " % (time_e - time_s))
#     HTML_Out2(DataJson, Recos_task,col,Times)


# 多task去重
# for col in Cols3:
#     time_s = time()
#     Recos_dedup = []
#     for task in tasks:
#         # print(task)
#         Recos = RecommendationWithTask(Data=DataJson, ColumnTypes=col, task=task, Num=0)
#         if not Recos is None:
#             for res in Recos:
#                 if res not in Recos_dedup:
#                     Recos_dedup.append(res)
#     Recos_dedup.sort()
#     time_e = time()
#     # print("Time last %f " % (time_e - time_s))
#     HTML_Out(DataJson, Recos_dedup, "china_city_de", col, time_e - time_s)


# print(BuildGraph(Recos,5))

# index = 1
# for ans in Recos:
#     print("index:%d" % (index))
#     print("Vega-Lite:", ans.props)
#     print("Cost:", ans.cost)
#     print("----------------------------")
#     index += 1


# ColumnTypes = [#rec-data.json
#     {"field": "datetime", "type": "temporal"},
#     {"field": "Time", "type": "quantitative"},
#     {"field": "status", "type": "quantitative"},
#     {"field": "temperature", "type": "quantitative"},
# ]


# ColumnTypes = [#Population_China.json
#     {"field": "Year", "type": "temporal"},
#     {"field": "Value", "type": "quantitative"},
#     {"field": "Country Name", "type": "nominal"},
#     # {"field": "Country Code", "type": "nominal"}
# ]

# ColumnTypes = [  # RFIDdata_4000.csv
#     {"field": "EPC", "type": "ordinal"},
#     # {"field": "Channel", "type": "ordinal"},
#     # {"field": "dopper", "type": "quantitative"},
#     {"field": "RSSI", "type": "quantitative"},
#     # {"field": "Phase", "type": "quantitative"},
#     {"field": "Time", "type": "temporal"},
# ]

# Cols=[
#     [# china_city.json
#     {'field': 'latitude', 'type': 'quantitative'},
#     {'field': 'longitude', 'type': 'quantitative'},
#     {'field': 'province', 'type': 'nominal'},
#     {'field': 'city', 'type': 'nominal'}
#     ]
# ]


# ColumnTypes = [  # tianyuan.json
#     {'field': 'CarID', 'type': 'nominal'},#车辆ID
#     {'field': 'Type', 'type': 'nominal'},#车型
#     {"field": "Tonnage", "type": "nominal"},#吨位
#     {"field": "Date", "type": "nominal"},#日期
#     {"field": "Time", "type": "temporal"},#当天工作时间
#     {"field": "Oil", "type": "quantitative"},#油耗
#     {"field": "Hours", "type": "quantitative"},#小时表
#     {'field': 'longitude', 'type': 'quantitative'},#经度
#     {'field': 'latitude', 'type': 'quantitative'},#纬度
# ]

# ColumnTypes = [  # tianyuan.json
#     # {'field': '车辆ID', 'type': 'nominal'},#
#     {'field': '车型', 'type': 'nominal'},#
#     {"field": "吨位", "type": "nominal"},#
#     # {"field": "日期", "type": "nominal"},#
#     {"field": "当天工作时间", "type": "temporal"},#
#     {"field": "油耗", "type": "quantitative"},#
#     {"field": "小时表", "type": "quantitative"},#
#     {'field': '经度', 'type': 'quantitative'},#
#     {'field': '纬度', 'type': 'quantitative'},#
# ]

# ColumnTypes = [#GDP_Avg_China.json
#     {'field': 'Value', 'type': 'quantitative'},
#     {'field': 'Year', 'type': 'ordinal'}
# ]

# ColumnTypes = [# china_city.json
#     {'field': 'latitude', 'type': 'quantitative'},
#     {'field': 'longitude', 'type': 'quantitative'},
#     {'field': 'province', 'type': 'nominal'},
#     {'field': 'city', 'type': 'nominal'}
# ]

# ColumnTypes = [# airports.json
#     {'field': 'latitude', 'type': 'quantitative'},
#     {'field': 'longitude', 'type': 'quantitative'},
#     {'field': 'state', 'type': 'nominal'},
#     {'field': 'city', 'type': 'nominal'},
#     {'field': 'country', 'type': 'nominal'},
#     # {'field': 'iata', 'type': 'nominal'}
# ]


# ColumnTypes = [
#     {'field': 'deathProbable', 'type': 'quantitative'},
#     {'field': 'date', 'type': 'ordinal'},
#     {'field': 'state', 'type': 'nominal'},
#     {'field': 'dataQualityGrade', 'type': 'nominal'},
#     {'field': 'death', 'type': 'quantitative'},
#     {'field': 'deathConfirmed', 'type': 'quantitative'},
#     {'field': 'deathIncrease', 'type': 'quantitative'}
# ]

# ColumnTypes = [#US_COVID
#     {'field': 'Lat', 'type': 'quantitative'},
#     {'field': 'Long', 'type': 'quantitative'},
#     # {'field': 'month', 'type': 'ordinal'},
#     # {'field': 'State', 'type': 'nominal'},
#     {'field': 'region', 'type': 'nominal'},
#     {'field': 'USMapID', 'type': 'nominal'},
#     {'field': 'death', 'type': 'quantitative'},
#     {'field': 'confirmed', 'type': 'quantitative'},
#     # {'field': 'Population', 'type': 'quantitative'},
#     {'field': 'date', 'type': 'temporal'}
# ]

# ColumnTypes = [#test
#     {'field': 'a', 'type': 'quantitative'},
#     {'field': 'ba', 'type': 'quantitative'},
#     {'field': 'test', 'type': 'nominal'}
# ]


# ColumnTypes = [#test
#     {'field': 'id', 'type': 'quantitative'},
#     {'field': 'Province', 'type': 'nominal'},
#     {'field': 'Year', 'type': 'quantitative'},
#     {'field': 'Value', 'type': 'quantitative'}
# ]
'''
Cols = [
    [{"field": "Origin", "type": "nominal"}],  # 0c1d

    [{"field": "Origin", "type": "nominal"},  # 0c2d
     {"field": "Year", "type": "ordinal"}],

    [{"field": "Origin", "type": "nominal"},  # 0c3d
     {"field": "Year", "type": "ordinal"},
     {"field": "Cylinders", "type": "ordinal"}],

    [{"field": "Acceleration", "type": "quantitative"}],  # 1c0d

    [{"field": "Acceleration", "type": "quantitative"},  # 1c1d
     {"field": "Origin", "type": "nominal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 1c2d
     {"field": "Origin", "type": "nominal"},
     {"field": "Year", "type": "ordinal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 1c3d
     {"field": "Origin", "type": "nominal"},
     {"field": "Year", "type": "ordinal"},
     {"field": "Cylinders", "type": "ordinal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 2c0d
     {"field": "Weight_in_lbs", "type": "quantitative"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 2c1d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Origin", "type": "nominal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 2c2d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Year", "type": "ordinal"},
     {"field": "Origin", "type": "nominal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 3c0d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Horsepower", "type": "quantitative"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 3c1d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Horsepower", "type": "quantitative"},
     {"field": "Origin", "type": "nominal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 3c2d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Horsepower", "type": "quantitative"},
     {"field": "Year", "type": "ordinal"},
     {"field": "Origin", "type": "nominal"}],

    [{"field": "Acceleration", "type": "quantitative"},  # 4c0d
     {"field": "Weight_in_lbs", "type": "quantitative"},
     {"field": "Displacement", "type": "quantitative"},
     {"field": "Horsepower", "type": "quantitative"}],
]

Cols2 = [  # tianyuan.json
    [  # cars.json
        # {"field": "Name", "type": "nominal"},
        # {"field": "Miles_per_Gallon", "type": "quantitative"},
        {"field": "Displacement", "type": "quantitative"},
        {"field": "Horsepower", "type": "quantitative"},
        # {'field': 'Weight_in_lbs', 'type': 'quantitative'},
        # {'field': 'Acceleration', 'type': 'quantitative'},
        {'field': 'Year', 'type': 'temporal'},
        {'field': 'Origin', 'type': 'nominal'},
        {"field": "Cylinders", "type": "ordinal"},
    ]
]

Cols3 = [[  # US_COVID
    {'field': 'Lat', 'type': 'quantitative'},
    {'field': 'Long', 'type': 'quantitative'},
    {'field': 'month', 'type': 'ordinal'},
    {'field': 'State', 'type': 'nominal'},
    {'field': 'USMapID', 'type': 'nominal'},
    {'field': 'death', 'type': 'quantitative'},
    {'field': 'confirmed', 'type': 'quantitative'},
    # {'field': 'Population', 'type': 'quantitative'},
    {'field': 'date', 'type': 'temporal'}
]
]
'''
