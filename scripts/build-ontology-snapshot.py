import sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'server'))
from ontology_backend import parse_ontology
v=parse_ontology((root/'ontology/mommis-aligned.owl').read_bytes())
v.update(source='Bundled OWL snapshot',status='snapshot')
(root/'explorer/data/ontology.json').write_text(json.dumps(v,indent=2))
from rdflib import Graph
Graph().parse(root/'ontology/mommis-aligned.owl',format='xml').serialize(root/'ontology/mommis-aligned.ttl',format='turtle')
print('Built ontology snapshot from ontology/mommis-aligned.owl')
