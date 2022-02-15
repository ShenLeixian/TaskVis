import pandas as pd
from time import time
from copy import deepcopy
from typing import List
from functools import reduce
from threading import Thread, Lock
from sklearn.cluster import DBSCAN
import numpy as np

from visrec.src.helper import *
from visrec.src.Transform import Asp2Vl, Cql2Asp, GetNewColumnType
from visrec.src.EditFunc import GetCost
from visrec.src.RunClingo import run
# from NLI.NLI import NL4DV
# from NLI.helpers import get_attributemap_for_NLP

task_rank = {
    'change_over_time': 3,
    'characterize_distribution': 1,
    'cluster': 1,
    'comparison': 1,
    'compute_derived_value': 1,
    'correlate': 1,
    'determine_range': 2,
    'deviation': 1,
    'error_range': 1,
    'find_anomalies': 3,
    'find_extremum': 1,
    'magnitude': 3,
    'part_to_whole': 1,
    'retrieve_value': 1,
    'sort': 1,
    'spatial': 2,
    'trend': 1,
    # 'filter',
}

task_name = {
    'change_over_time': "时序变化",
    'characterize_distribution': "分布",
    'cluster': "聚类",
    'comparison': "对比",
    'compute_derived_value': "推导值",
    'correlate': "关系",
    'determine_range': "取值范围",
    'deviation': "偏差",
    'error_range': "误差",
    'find_anomalies': "异常值",
    'find_extremum': "极值",
    'magnitude': "大小",
    'part_to_whole': "部分与整体",
    'retrieve_value': "取值",
    'sort': "排序",
    'spatial': "空间",
    'trend': "趋势",
}
tasks = list(task_rank.keys())

Recos_dedup = []
lock = Lock()


'''Individual Recommendation'''
def rank(new,rankscheme,ColumnTypes={}):
    news=deepcopy(new)
    if rankscheme == 1:  # Complexity-based
        for item in news:
            item.count=1
        news.sort()
    elif rankscheme == 2:  # Reverse-complexity-based
        news.sort()
        cost = []
        for item in news:
            cost.append([item.cost, 0])
        cost = np.asarray(cost)
        label = DBSCAN(eps=0.5, min_samples=1).fit_predict(cost)
        label = list(label)
        clusters = list(set(label))
        costmean = [0]*len(clusters)
        for i in range(len(news)):
            costmean[label[i]] += news[i].cost
        for i in range(len(costmean)):
            costmean[i] /= label.count(i)
        costmean_reverse = deepcopy(costmean)
        costmean_reverse.reverse()
        for i in range(len(costmean)):
            costmean[i] -= costmean_reverse[i]
        for i in range(len(news)):
            news[i].cost -= costmean[label[i]]
        news.sort()
    elif rankscheme == 3:  # Interested-columns-based
        for item in news:
            item.cost /= (len(item.fields)/len(ColumnTypes))
        news.sort()
    elif rankscheme == 4:  # Task-coverage-based
        news.sort()
    return news

def IndivRecWithSingleTask(Data, ColumnTypes={}, task=None,DataAsp=None, Num=10):
    # print(task)
    if DataAsp is None:
        dataquery = data_to_asp(Data, ColumnTypes)
    else:
        dataquery=DataAsp

    header = list(ColumnTypes.keys())
    query_spec = {'data': {'url': "./values"}}
    query_spec['encodings'] = []
    for item in header:
        query_spec['encodings'].append({"field": item, "type": ColumnTypes[item]})
    query = Cql2Asp(query_spec)
    if not task is None:
        query.append('task(%s).' % (task))
    program = query + dataquery
    # print("program!:",program)
    result = run(draco_query=program, num=Num)

    if result is None:
        # print("No Answers!")
        return None

    for ans in result:
        ans.Ops = ans.props
        ans.props, ans.cost = Asp2Vl(ans.props, task)
        ans.cost, ans.fields = GetCost(ans.props, task)
        ans.props=DeLayer(ans.props)
    news = reduce(lambda x, y: x if y in x else x + [y], [[], ] + result)
        
    # print("After deduplication, left %d vis:" % (len(news)))
    news.sort()
    return news
    '''
    rankscheme = task_rank[task]
    if rankscheme == 1:  # Complexity-based
        news.sort()
    elif rankscheme == 2:  # Reverse-complexity-based
        news.sort()
        cost = []
        for item in news:
            cost.append([item.cost, 0])
        cost = np.asarray(cost)
        label = DBSCAN(eps=0.5, min_samples=1).fit_predict(cost)
        label = list(label)
        clusters = list(set(label))
        costmean = [0]*len(clusters)
        for i in range(len(news)):
            costmean[label[i]] += news[i].cost
        for i in range(len(costmean)):
            costmean[i] /= label.count(i)
        costmean_reverse = deepcopy(costmean)
        costmean_reverse.reverse()
        for i in range(len(costmean)):
            costmean[i] -= costmean_reverse[i]
        for i in range(len(news)):
            news[i].cost -= costmean[label[i]]
        news.sort()
    elif rankscheme == 3:  # Interested-columns-based
        for item in news:
            item.cost /= (len(item.fields)/len(ColumnTypes))
        news.sort()
    elif rankscheme == 4:  # Task-coverage-based
        news.sort()
    # PrintVegaLite(news)
    return news
    '''

def Result2Json(res_):
    res=deepcopy(res_)
    task_res = []
    for ans in res:
        res_dict = {
            "props": ans.props,
            "cost": ans.cost,
            "field":list(ans.fields),
            "task": list(ans.task)
        }
        task_res.append(res_dict)
    return task_res

def IndivRecWithoutTask(Data, ColumnTypes={},DataAsp=None, Num=10):
    return RecommendationCombination(Data=Data, ColumnTypes=ColumnTypes, Num=Num,DataAsp=DataAsp, task_list=None)


def IndivRecWithMultiTasks(Data, ColumnTypes={}, task=[],DataAsp=None, Num=10,mode=2):
    if len(task) == 0:
        return RecommendationCombination(Data=Data, ColumnTypes=ColumnTypes, Num=Num,DataAsp=DataAsp, task_list=None,mode=mode)
    else:
        return RecommendationCombination(Data=Data, ColumnTypes=ColumnTypes, Num=Num,DataAsp=DataAsp, task_list=task,mode=mode)


def RecommendationCombination(Data, ColumnTypes={},DataAsp=None,Num=10, task_list=None,mode=2):
    global Recos_dedup
    final_res={}
    Recos_dedup = []
    Recos_nodedup={}
    tasklist = tasks if task_list is None else task_list

    def process(start, end):
        for i in range(start, end):
            if not tasklist[i] in tasks:
                raise Exception(print("No %s Task!" % (tasklist[i])))
            Recos = IndivRecWithSingleTask(Data=Data, ColumnTypes=ColumnTypes,DataAsp=DataAsp, task=tasklist[i], Num=0)
            if not Recos is None:
                if mode==2:
                    res_with_rank={}
                    res_with_rank['R1']=Result2Json(Recos)
                    try:
                        res_with_rank['R2']=Result2Json(rank(Recos,2,ColumnTypes))
                    except:
                        res_with_rank['R2']=Result2Json(list(reversed(Recos)))
                    res_with_rank['R3']=Result2Json(rank(Recos,3,ColumnTypes))
                    res_with_rank['R4']=Result2Json(Recos)
                    Recos_nodedup[tasklist[i]]=res_with_rank
                for res in Recos:
                    lock.acquire()
                    if res not in Recos_dedup:
                        res.count = 1
                        res.task.add(tasklist[i])
                        Recos_dedup.append(res)
                    else:
                        Recos_dedup[Recos_dedup.index(res)].count += 1
                        Recos_dedup[Recos_dedup.index(res)].cost += res.cost
                        Recos_dedup[Recos_dedup.index(res)].task.add(tasklist[i])
                    lock.release()
    n = 8
    start = end = 0
    threads = []
    for i in range(n):
        start = end
        end = int((i+1)/n*len(tasklist))
        th = Thread(target=process, args=(start, end))
        threads.append(th)
        th.start()
    for t in threads:
        t.join()

    for item in Recos_dedup:
        item.cost /= item.count
    Recos_dedup.sort()

    if mode==2:
        res_with_rank2={}
        res_with_rank2['R1']=Result2Json(rank(Recos_dedup,1,ColumnTypes))
        try:
            res_with_rank2['R2']=Result2Json(rank(Recos_dedup,2,ColumnTypes))
        except:
            res_with_rank2['R2']=Result2Json(list(reversed(rank(Recos_dedup,1,ColumnTypes))))
        res_with_rank2['R3']=Result2Json(rank(Recos_dedup,3,ColumnTypes))
        res_with_rank2['R4']=Result2Json(rank(Recos_dedup,4,ColumnTypes))
    
        final_res['Recos_dedup']=res_with_rank2
        final_res['Recos_nodedup']=Recos_nodedup
        return final_res
    else:
        if Num == 0:
            Num = len(Recos_dedup)
        elif Num > len(Recos_dedup):
            Num = len(Recos_dedup)
        # PrintVegaLite(Recos_dedup[0:Num])
        return Recos_dedup[0:Num]


'''Combination Recommendation'''

class Dashboard:
    def __init__(self):
        self.pics = []
        self.Fields = set()
        self.TaskCount = 0
        self.TaskCover = set()
        self.Cost = 0

    def __lt__(self, other):
        if self.TaskCount < other.TaskCount:
            return True
        elif self.TaskCount > other.TaskCount:
            return False
        elif self.Cost > other.Cost:
            return True
        return False

    def __eq__(self, other):
        return self.Fields == other.Fields

def CombinationRecommendation(Data, ColumnTypes={}, task=[],DataAsp=None, mode=5):
    # if mode == 4:
    #     Recos_dedup = IndivRecWithoutTask(Data=Data, ColumnTypes=ColumnTypes,DataAsp=DataAsp, Num=0)
    # elif mode == 5:
    Recos_dedup = IndivRecWithMultiTasks(Data=Data, ColumnTypes=ColumnTypes, task=task,DataAsp=DataAsp, Num=0,mode=mode)
    # elif mode == 6:
    #     Recos_dedup = IndivRecWithSingleTask(Data=Data, ColumnTypes=ColumnTypes, task=task,DataAsp=DataAsp, Num=0)
    # else:
    #     raise Exception(print("No %s Mode!" % (mode)))
    Recos_dedup = GetUniqueFields(Recos_dedup)
    Len = len(Recos_dedup)
    if Len == 0:
        return
    Columns = list(ColumnTypes.keys())
    clen = len(Columns)
    ANS = []
    DynamicCol = []
    while len(DynamicCol) < clen and len(Recos_dedup) > 0:
        chosen = Recos_dedup[0]
        ANS.append(chosen)
        if len(chosen.fields) == 1:
            Recos_dedup = DeleteIter(chosen.fields, Recos_dedup)
        elif len(chosen.fields) > 1:
            DynamicCol = list(set(DynamicCol).union(chosen.fields))
            Recos_dedup = DeleteIter(DynamicCol, Recos_dedup)
            # Recos_dedup = DeleteIter(list(chosen.fields),Recos_dedup)
    return Result2Json(ANS)


def TaskVisAPIs(Data, ColumnTypes: List[dict] = [], task=None,DataAsp=None, Num=10, mode=1):
    ColumnDict = {}
    if type(Data) is list:
        Data = pd.DataFrame(Data)
    elif type(Data) is pd.DataFrame:
        pass
    else:
        raise Exception(print("Data invaild."))
    # print(ColumnTypes)
    if len(ColumnTypes) == 0:
        keys = list(Data.columns)
        for key in keys:
            ColumnDict[key] = 'unknown'
    elif len(ColumnTypes[0]) == 1:
        for item in ColumnTypes:
            ColumnDict[item['field']] = 'unknown'
    else:
        for item in ColumnTypes:
            ColumnDict[item['field']] = item['type']
    Data = Data[list(ColumnDict.keys())]
    ColumnDict=GetNewColumnType(Data,ColumnDict)

    # mode 1:Individual recommendation with single task
    if mode == 1:
        if type(task) !=str:
            raise Exception(print("Must input single task string in SingleTask mode!"))
        recos= IndivRecWithSingleTask(Data=Data, ColumnTypes=ColumnDict, task=task,DataAsp=DataAsp, Num=0)
    # mode 2:Individual recommendation with multiple tasks
    elif mode == 2:
        if type(task) !=list:
            raise Exception(print("Must input task list in MultiTask mode!"))
        recos= IndivRecWithMultiTasks(Data=Data, ColumnTypes=ColumnDict, task=task,DataAsp=DataAsp, Num=0)
    # mode 3:Individual recommendation without task
    elif mode == 3:
        recos= IndivRecWithoutTask(Data=Data, ColumnTypes=ColumnDict,DataAsp=DataAsp, Num=0)
    # mode 4:Combination recommendation without task
    elif mode == 4:
        recos= CombinationRecommendation(Data=Data, ColumnTypes=ColumnDict,DataAsp=DataAsp, mode=4)
    # mode 5:Combination recommendation with multiple tasks
    elif mode == 5:
        if type(task) !=list:
            raise Exception(print("Must input task list in MultiTask mode!"))
        recos= CombinationRecommendation(Data=Data, ColumnTypes=ColumnDict, task=task,DataAsp=DataAsp, mode=5)
    # mode 6:Combination recommendation with single task
    elif mode == 6:
        if type(task) !=str:
            raise Exception(print("Must input single task string in SingleTask mode!"))
        recos= CombinationRecommendation(Data=Data, ColumnTypes=ColumnDict, task=task,DataAsp=DataAsp, mode=6)
    else:
        raise Exception(print("No %s Mode!" % (mode)))

    # for ans in recos:
    #     ans.props=DeLayer(ans.props)

    df = Data.where((pd.notnull(Data)), None)
    df = list(df.T.to_dict().values())
    return recos,df