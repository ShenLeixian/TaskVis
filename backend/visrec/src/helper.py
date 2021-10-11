import pandas as pd
from copy import deepcopy
from visrec.src.Transform import Data2Schema, Schema2Asp
import itertools


def data_to_asp(data: pd.DataFrame, ColumnTypes: dict = {}):
    return Schema2Asp(Data2Schema(data, ColumnTypes))

def GetFields(Recos):
    res = deepcopy(Recos)
    for item in res:
        Match = set()
        d = {}
        for encode in item.props['layer']:
            d.update(encode['encoding'])
        keys = d.keys()
        for key in keys:
            # if d[key].__contains__('field') and not d[key]['field'] in Match:
            # Match.append(d[key]['field'])
            if d[key].__contains__('field'):
                Match.add(d[key]['field'])
        item.fields = Match
    return res


def PrintVegaLite(Recos):
    index = 1
    for ans in Recos:
        print("index:%d" % (index))
        print("Vega-Lite:", ans.props)
        # print("Asp:", ans.Ops)
        print("Fields:", ans.fields)
        # print("TaskCount:", ans.count)
        # print("Tasks:", ans.task)
        print("Cost:", ans.cost)
        print("----------------------------")
        index += 1


def GetIters(lst):
    combs = []
    for i in range(1, len(lst)+1):
        els = [list(x) for x in itertools.combinations(lst, i)]
        combs.extend(els)
    return combs


def DeleteIter(column, Recos):
    columns = GetIters(sorted(column))
    NewRecos = []
    for item in Recos:
        if not sorted(list(item.fields)) in columns:
            NewRecos.append(item)
    return NewRecos


def GetUniqueFields(Recos):
    deRecos = []
    field = []
    taskcount = []
    # cost=[]
    for item in Recos:
        if not item.fields in field:
            field.append(item.fields)
            taskcount.append(item.count)
            # cost.append(item.cost)
            deRecos.append(item)
    # return deRecos,field,taskcount
    return deRecos

def DeLayer(props):
    if len(props["layer"])<2:
        props.update(props.pop("layer")[0])
        return props
    return props

def word2vec(word):
    from collections import Counter
    from math import sqrt
    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))
    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

# def read_data_to_asp(file: str, ColumnTypes: dict = {}):
#     header = list(ColumnTypes.keys())
#     if file.endswith(".json"):
#         with open(file) as f:
#             data = json.load(f)
#             data = pd.DataFrame(data)
#             data = data[header]
#             df = data.where((pd.notnull(data)), None)
#             df = list(df.T.to_dict().values())
#             return Schema2Asp(Data2Schema(data, ColumnTypes)[0],Data2Schema(data, ColumnTypes)[1]), df
#     elif file.endswith(".csv"):
#         data = pd.read_csv(file, encoding='utf-8')
#         data = data[header]
#         df = data.where((pd.notnull(data)), None)
#         df = list(df.T.to_dict().values())
#         schema = Data2Schema(data, ColumnTypes)
#         asp = Schema2Asp(schema,ColumnTypes)
#         return asp, df
#     else:
#         raise Exception("invalid file type")

# def GetUniqueFields2(Recos):
#     deRecos=[]
#     field=[]
#     taskcount=[]
#     field_task=[]
#     for item in Recos:
#         temp=list(item.fields)+list(item.task)
#         if not temp in field_task:
#             field_task.append(temp)
#             field.append(item.fields)
#             taskcount.append(item.count)
#             # cost.append(item.cost)
#             deRecos.append(item)
#     return deRecos,field,taskcount

# def getTempCost(fields,maxtasks,Column):
#     taskscount=0
#     if Column in fields:
#         taskscount+=maxtasks[fields.index(Column)]
#     return taskscount
