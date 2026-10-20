"""Extract JSON literals from supplied HTML without executing its JavaScript."""
import json,re,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];folder=root/'explorer/knowledge-graph'
raw=(folder/'source/original.html').read_bytes();text=raw.decode('utf-8')
data={key:json.loads(re.search(r'const '+var+r' = (.*);',text).group(1)) for key,var in [('nodes','allNodes'),('edges','allEdges')]}
ids={n['id'] for n in data['nodes']}
assert len(ids)==len(data['nodes'])
assert len({e['id'] for e in data['edges']})==len(data['edges'])
assert all(e['from'] in ids and e['to'] in ids for e in data['edges'])
data['provenance']={'source':'source/original.html','sha256':hashlib.sha256(raw).hexdigest(),'status':'Imported source labels, not independently validated','importedOn':'2026-10-20'}
encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
(folder/'index.html').write_text((folder/'viewer.template.html').read_text().replace('__GRAPH_DATA__',encoded))
print('Built self-contained graph:',len(data['nodes']),'entities,',len(data['edges']),'relationships')
