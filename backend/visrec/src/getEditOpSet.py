import pandas as pd
import json
import re

with open('./visrec/lp/costs.json') as f:
    costs = json.load(f)
with open('./visrec/lp/idMap.json') as f:
    idMap = json.load(f)
maxEncodingCost = 0
depth=10
editOpNames = list(idMap.keys())
editOpSet = {
    'markEditOps': {},
    'transformEditOps': {},
    'encodingEditOps':{},
    'retrieve_value': {},
    'filter': {},
    'compute_derived_value': {},
    'find_extremum': {},
    'sort': {},
    'determine_range': {},
    'characterize_distribution': {},
    'find_anomalies': {},
    'cluster': {},
    'correlate': {},
    'part_to_whole': {},
    'change_over_time': {},
    'magnitude': {},
    'comparison': {},
    'spatial': {},
    'deviation': {},
    'trend': {},
    'error_range': {}
}
for i in range(len(editOpNames)):
  if i <= 14:
    editOpSet['markEditOps'][editOpNames[i]] = { 'name': editOpNames[i], 'cost': costs[i] }
  elif i <= 27:
    editOpSet['transformEditOps'][editOpNames[i]] = { 'name': editOpNames[i], 'cost': costs[i] }
  elif i<=147:
    if maxEncodingCost < costs[i]:
      maxEncodingCost = costs[i]
    editOpSet['encodingEditOps'][editOpNames[i]] = { 'name': editOpNames[i], 'cost': costs[i] }
  else :
    pattern = r"(.*)__(.*)"
    match = re.match(pattern, editOpNames[i], re.M | re.I)
    editOpSet[match[1]][editOpNames[i]] = { 'name': editOpNames[i], 'cost': costs[i] }

editOpSet['encodingEditOps']['ceiling'] = {
  'cost': maxEncodingCost * depth,
  'alternatingCost': maxEncodingCost * ( depth + 1 )
}

editkeys=list(editOpSet.keys())
for edit in editkeys:
  if not edit in['markEditOps','transformEditOps','encodingEditOps']:
    keys=list(editOpSet[edit].keys())
    for i in range(len(keys)):
      editOpSet[edit][keys[i]]['cost']=0.01*(i+1)

