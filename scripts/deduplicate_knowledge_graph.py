"""Conservative, reproducible entity deduplication; retain original assertions."""
from collections import defaultdict, Counter
from copy import deepcopy
import re
import unicodedata

# Reviewed same-type, same-identifier singular/plural or punctuation variants.
SAFE_IDS = {'CHEBI:147155','CHEBI:75769','CHEBI:16646','CHEBI:28892',
            'CHEBI:167559','CHEBI:18059','CHEBI:59520','CHEBI:50699',
            'CHEBI:16670','CHEBI:36080','CHEBI:26667','CHEBI:26739'}

def normalize(label, group):
    label = unicodedata.normalize('NFKC', label)
    label = label.translate(str.maketrans({'′':"'",'’':"'",'‘':"'",'–':'-','‑':'-','−':'-'}))
    # Unit case can change a measurement's meaning.
    if group != 'Measurement':
        label = label.casefold()
    return re.sub(r'\s+', ' ', label).strip()

def deduplicate(data):
    original = deepcopy(data)
    nodes = data['nodes']; parent = list(range(len(nodes)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    def union(indices):
        ids = {nodes[i].get('ontology_id') for i in indices} - {None, ''}
        if len(ids) > 1: return
        for i in indices[1:]: parent[root(i)] = root(indices[0])
    keys = defaultdict(list)
    for i,n in enumerate(nodes):
        keys[(n['group'],normalize(n['label'],n['group']))].append(i)
    for indices in keys.values(): union(indices)
    keys = defaultdict(list)
    for i,n in enumerate(nodes):
        if n.get('ontology_id') in SAFE_IDS:
            keys[(n['group'],n['ontology_id'])].append(i)
    for indices in keys.values(): union(indices)
    clusters = defaultdict(list)
    for i,n in enumerate(nodes): clusters[root(i)].append(n)
    result=[]; crosswalk={}; merges=[]
    for members in clusters.values():
        canonical = max(members,key=lambda n:(bool(n.get('mapped')),n.get('mapping_confidence',0),n.get('degree',0)))
        n=deepcopy(canonical)
        n['aliases']=sorted({m['label'] for m in members if m['label']!=n['label']})
        n['original_ids']=[m['id'] for m in members]
        n['sources']=sorted({s for m in members for s in m.get('sources',[])})
        for m in members: crosswalk[m['id']]=n['id']
        if len(members)>1:
            n['original_records']=deepcopy(members)
            merges.append({'canonical':n['id'],'original_ids':n['original_ids']})
        result.append(n)
    edges=[]; seen={}
    for old in original['edges']:
        e=deepcopy(old); e['from']=crosswalk[e['from']]; e['to']=crosswalk[e['to']]
        # Evidence, sources, pages, scores and status are part of assertion identity.
        import json
        key=json.dumps({k:v for k,v in e.items() if k not in ('id','subject_mapped','object_mapped')},sort_keys=True)
        if key in seen:
            seen[key]['original_assertions'].append(old)
        else:
            e['original_assertions']=[old]; seen[key]=e; edges.append(e)
    degree=Counter()
    byid={n['id']:n for n in result}
    for e in edges:
        degree.update({e['from'],e['to']})
        e['subject_mapped']=bool(byid[e['from']].get('mapped'))
        e['object_mapped']=bool(byid[e['to']].get('mapped'))
    for n in result: n['degree']=degree[n['id']]
    mappings=defaultdict(list)
    for n in result:
        if n.get('ontology_id'): mappings[n['ontology_id']].append(n['id'])
    report={'input_entities':len(nodes),'output_entities':len(result),
            'input_assertions':len(original['edges']),'output_assertions':len(edges),
            'merges':merges,'mapping_conflicts':{k:v for k,v in mappings.items() if len(v)>1}}
    data['nodes']=result; data['edges']=edges; data['deduplication']=report
    return report
