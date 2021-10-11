from copy import deepcopy
import queue
from visrec.src.getEditOpSet import editOpSet

def MarkEditOps(s, d,task=None):
    editOps = []
    if s['layer'][0]['mark']['type'] == d['layer'][0]['mark']['type']:
        return editOps
    elif task != None:
        if s['layer'][0]['mark']['type'] == '':
            editOpName=task+'__'+d['layer'][0]['mark']['type']
            if(editOpName in editOpSet[task]):
                newEditOp = editOpSet[task][editOpName]
                # newEditOp['detail']={ "before": s['mark'].upper(), "after": d['mark'].upper()}
                editOps.append(newEditOp)
        else:
            editOpName_ = [s['layer'][0]['mark']['type'].upper(), d['layer'][0]['mark']['type'].upper()]
            editOpName_.sort()
            editOpName = "_".join(editOpName_)
            if(editOpName in editOpSet['markEditOps']):
                newEditOp = editOpSet['markEditOps'][editOpName]
                # newEditOp['detail']={ "before": s['mark'].upper(), "after": d['mark'].upper()}
                editOps.append(newEditOp)
    return editOps


def TransformEditOps(ss, dd):
    editOps = []

    ts = deepcopy(ss)['layer']
    s={}
    for encode in ts:
        s.update(encode['encoding'])
    for item in ts:
        if 'transform' in item.keys():
            s['transform']=item['transform'][0]
    
    td = deepcopy(dd)['layer']
    d={}
    for encode in td:
        d.update(encode['encoding'])
    for item in td:
        if 'transform' in item.keys():
            d['transform']=item['transform'][0]

    transform = ['aggregate', 'bin', 'sort', 'stack','loess','regression']  # 'scale',
    skeys = list(s.keys())
    dkeys = list(d.keys())
    InterKeys = list(set(dkeys).intersection(set(skeys)))
    DifKeys_ds = list(set(dkeys).difference(set(skeys)))
    DifKeys_sd = list(set(skeys).difference(set(dkeys)))
    # print(InterKeys,DifKeys_ds,DifKeys_sd)
    for c in InterKeys:
        for t in transform:
            if t in list(s[c].keys()) and t in list(d[c].keys()):
                continue
            elif not t in list(s[c].keys()) and not t in list(d[c].keys()):
                continue
            else:
                editOpName = t.upper()
                if editOpName == 'AGGREGATE':
                    editOpName=editOpName+'_'+s[c]['aggregate'].upper()
                elif editOpName == 'STACK':
                    editOpName=editOpName+'_'+s[c]['stack'].upper()
                if editOpName in editOpSet['transformEditOps'] and not editOpName in editOps:
                    editOps.append(editOpSet['transformEditOps'][editOpName])
    for c in DifKeys_sd:
        for t in transform:
            if t in list(s[c].keys()):
                editOpName = t.upper()
                if editOpName == 'AGGREGATE':
                    editOpName=editOpName+'_'+s[c]['aggregate'].upper()
                elif editOpName == 'STACK':
                    editOpName=editOpName+'_'+s[c]['stack'].upper()
                if editOpName in editOpSet['transformEditOps'] and not editOpName in editOps:
                    editOps.append(editOpSet['transformEditOps'][editOpName])
    for c in DifKeys_ds:
        for t in transform:
            if t in list(d[c].keys()):
                editOpName = t.upper()
                if editOpName == 'AGGREGATE':
                    editOpName=editOpName+'_'+d[c]['aggregate'].upper()
                elif editOpName == 'STACK':
                    editOpName=editOpName+'_'+d[c]['stack'].upper()
                if editOpName in editOpSet['transformEditOps'] and not editOpName in editOps:
                    editOps.append(editOpSet['transformEditOps'][editOpName])
    return editOps



def RemoveTransform(result_):
    result = deepcopy(result_)
    result.props = result.props['layer']
    d={}
    for encode in result.props:
        d.update(encode['encoding'])
    # for item in result.props:
    #     if 'transform' in item.keys():
    #         d['transform']=item['transform'][0]
    result.props=d
    C = list(d.keys())
    for item in C:
        try:
            result.props[item] = {'field': result.props[item]['field']}
        except:
            if item == 'y':
                result.props[item] = {'field': result.props['x']['field']}
    #     if 'scale' in list(result.props[item].keys()):
    #         result.props[item].pop('scale')
    #     if 'aggregate' in list(result.props[item].keys()):
    #         result.props[item].pop('aggregate')
    #     if 'type' in list(result.props[item].keys()):
    #         result.props[item].pop('type')
    return result


def GetInitCost(s, d):
    skeys = list(s.keys())
    dkeys = list(d.keys())
    cost = 0
    InterKeys = list(set(dkeys).intersection(set(skeys)))
    DifKeys_ds = list(set(dkeys).difference(set(skeys)))
    DifKeys_sd = list(set(skeys).difference(set(dkeys)))
    for c in InterKeys:
        editOpName = 'MODIFY_'+c.upper()
        if(editOpName in editOpSet['encodingEditOps']):
            cost += editOpSet['encodingEditOps'][editOpName]['cost']
            # print(editOpName,cost)
    for c in DifKeys_sd:
        editOpName = 'REMOVE_'+c.upper()
        if(editOpName in editOpSet['encodingEditOps']):
            cost += editOpSet['encodingEditOps'][editOpName]['cost']
            # print(editOpName,cost)
    for c in DifKeys_ds:
        editOpName = 'ADD_'+c.upper()
        if(editOpName in editOpSet['encodingEditOps']):
            cost += editOpSet['encodingEditOps'][editOpName]['cost']
            # print(editOpName,cost)
    return cost


def GetGraphPara(s, d):
    GraphPara = {'ADD': [], 'REMOVE': [],
                 'MODIFY': [], 'MOVE_be': [], 'MOVE_af': []}
    skeys = list(s.keys())
    dkeys = list(d.keys())
    GraphPara['ADD'] = dkeys
    GraphPara['MODIFY'] = skeys
    GraphPara['REMOVE'] = skeys
    GraphPara['MOVE_be'] = skeys
    GraphPara['MOVE_af'] = dkeys
    return GraphPara


def EncodingEditOps(start, destination):
    s = RemoveTransform(start)
    d = RemoveTransform(destination)
    dkeys = list(d.props.keys())
    mincost = GetInitCost(s.props, d.props)
    EditOps = []
    # visited = []
    q = queue.Queue()
    q.put(s)
    # visited.append(s.props)
    # PriorityPara = {'ADD': 4, 'REMOVE': 3, 'MODIFY': 3, 'MOVE_be': 2, 'MOVE_af': 2}
    while not q.empty():
        u = q.get()
        # print("-----------------")
        # print(q.qsize())
        # print(u.props)
        # print(u.Ops)
        if u.cost > mincost:
            continue
        if u.props == d.props:
            if u.cost < mincost:
                mincost = u.cost
                EditOps = u.Ops
            elif u.cost == mincost:
                EditOps = u.Ops
            continue
        GraphPara = GetGraphPara(u.props, d.props)
        skeys = list(u.props.keys())
        # print(GraphPara)
        # print("skeys:",GraphPara["REMOVE"])
        # print("dkeys:",GraphPara["ADD"])
        for k, v in GraphPara.items():
            if k == 'ADD':
                for c in v:
                    T = deepcopy(u)
                    if not c in skeys:
                        T.props[c] = d.props[c]
                        # if not T.props in visited:
                        # visited.append(T.props)
                        editOpName = 'ADD_'+c.upper()
                        if(editOpName in editOpSet['encodingEditOps']):
                            T.cost += editOpSet['encodingEditOps'][editOpName]['cost']
                            T.Ops.append(editOpSet['encodingEditOps'][editOpName])
                            q.put(T)
            elif k == 'REMOVE':
                for c in v:
                    T = deepcopy(u)
                    if not c in dkeys:
                        T.props.pop(c)
                        # if not T.props in visited:
                        # visited.append(T.props)
                        editOpName = 'REMOVE_'+c.upper()
                        if(editOpName in editOpSet['encodingEditOps']):
                            T.cost += editOpSet['encodingEditOps'][editOpName]['cost']
                            T.Ops.append(editOpSet['encodingEditOps'][editOpName])
                            q.put(T)
            elif k == 'MODIFY':
                for c in v:
                    T = deepcopy(u)
                    if c in dkeys:
                        T.props[c] = d.props[c]
                        # if not T.props in visited:
                        # visited.append(T.props)
                        editOpName = 'MODIFY_'+c.upper()
                        if(editOpName in editOpSet['encodingEditOps']):
                            T.cost += editOpSet['encodingEditOps'][editOpName]['cost']
                            T.Ops.append(editOpSet['encodingEditOps'][editOpName])
                            q.put(T)
            elif k == 'MOVE_be':
                v_be = GraphPara['MOVE_be']
                v_af = GraphPara['MOVE_af']
                for c1 in v_be:
                    for c2 in v_af:
                        T = deepcopy(u)
                        if c1 != c2 and T.props[c1] == d.props[c2] and not c2 in skeys:
                            T.props[c2] = T.props.pop(c1)
                            # if not T.props in visited:
                            # visited.append(T.props)
                            editOpName = 'MOVE_'+c1.upper()+'_'+c2.upper()
                            if(editOpName in editOpSet['encodingEditOps']):
                                T.cost += editOpSet['encodingEditOps'][editOpName]['cost']
                                T.Ops.append(
                                    editOpSet['encodingEditOps'][editOpName])
                                q.put(T)
    return EditOps


### just get cost ###
def MarkEditCost(d,task=None):
    cost=0
    if task != None:
        editOpName=task+'__'+d['layer'][0]['mark']['type']
        if(editOpName in editOpSet[task]):
            cost+=editOpSet[task][editOpName]['cost']
    return cost

def TransformEditCost(dd):
    editOps=[]
    Match = set()
    td = deepcopy(dd)['layer']
    d={}
    for encode in td:
        d.update(encode['encoding'])
    for item in td:
        if 'transform' in item.keys():
            d['transform']=item['transform'][0]

    transform = ['aggregate', 'bin', 'sort', 'stack','loess','regression']  # 'scale',
    dkeys = list(d.keys())
    for c in dkeys:
        for t in d[c].keys():
            if t in transform:
                editOpName = t.upper()
                if editOpName == 'AGGREGATE':
                    editOpName=editOpName+'_'+d[c]['aggregate'].upper()
                elif editOpName == 'STACK':
                    editOpName=editOpName+'_'+d[c]['stack'].upper()
                if editOpName in editOpSet['transformEditOps'] and not editOpName in editOps:
                    editOps.append(editOpSet['transformEditOps'][editOpName])
            elif t =='field':
                Match.add(d[c]['field'])
    
    cost=0
    if td[0]["mark"]["type"]=="geoshape":
        try:
            op=td[0]["transform"][1]["window"][0]["op"]
            editOpName='AGGREGATE'+'_'+op.upper()
            if editOpName in editOpSet['transformEditOps'] and not editOpName in editOps:
                editOps.append(editOpSet['transformEditOps'][editOpName])
        except:
            pass
        ma=list(Match)
        for item in ma:
            if item.startswith("mean of ") or item.startswith("sum of "):
                tt=item.split()[2]
                ma.remove(item)
                ma.append(tt)
        Match=set(ma)

    for trans in editOps:
        cost+=trans['cost']
    return cost,Match

def EncodingEditCost(dd):
    editOps=[]
    td = deepcopy(dd)['layer']
    d={}
    for encode in td:
        d.update(encode['encoding'])

    encoding = ['x', 'y', 'color', 'size','shape','latitude','longitude','theta']
    dkeys = list(d.keys())
    for c in dkeys:
        if c in encoding:
            editOpName = 'ADD_'+c.upper()
            if editOpName in editOpSet['encodingEditOps'] and not editOpName in editOps:
                editOps.append(editOpSet['encodingEditOps'][editOpName])
    cost=0
    for en in editOps:
        cost+=en['cost']        
    return cost

def GetCost(destination,task=None):
    cost = 0
    cost+=MarkEditCost(destination,task)
    Tcost,Match=TransformEditCost(destination)
    cost+=Tcost
    cost+=EncodingEditCost(destination)
    return cost,Match
