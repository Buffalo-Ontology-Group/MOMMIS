"""Build contextual RDF, saved SPARQL answers and the offline MVP from its editable sources."""
import json,sys,csv,io
from pathlib import Path
from rdflib import Graph,Namespace,URIRef,Literal,RDF,RDFS
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'server'))
from ontology_backend import parse_ontology
D=ROOT/'explorer/data'; data=json.loads((D/'mvp.json').read_text())
M=Namespace('https://w3id.org/mommis/mvp/');g=Graph();g.bind('mvp',M)
for n in data['entities']:
 s=M[n['id']];g.add((s,RDFS.label,Literal(n['label'])));g.add((s,M.kind,Literal(n['kind'])))
 if n.get('ontologyIRI'):g.add((s,M.candidateMapping,URIRef(n['ontologyIRI'])))
for n in data['glycans']:
 for field in ['glytoucan','wurcs','milkOligoId','mappingStatus']:g.add((M[n['id']],M[field],Literal(n[field])))
for r in data['records']:
 s=M[r['id']];g.add((s,RDF.type,M.EvidenceAssertion))
 g.add((s,RDF.subject,M[r['subject']]));g.add((s,RDF.predicate,M.reportsEndpoint));g.add((s,RDF.object,M[r['target']]))
 for key in ['title','statement','system','model','strain','exposure','comparator','dose','duration','reviewStatus','sourceLocation','origin','limitation','stageKey']:
  g.add((s,M[key],Literal(r[key])))
 for id in r['glycanIds']:g.add((s,M.glycan,M[id]))
 source=next(x for x in data['sources'] if x['id']==r['sourceId']);g.add((s,M.source,URIRef(source['url'])))
 if r.get('ontologyIRI'):g.add((s,M.candidateMapping,URIRef(r['ontologyIRI'])))
# Reified evidence only: never assert a universal molecule -> health effect triple.
g.serialize(D/'mvp.ttl',format='turtle')
answers=[]
for p in sorted((ROOT/'queries').glob('*.rq')):
 result=g.query(p.read_text());columns=[str(x) for x in result.vars];rows=[[str(x) if x is not None else '' for x in r] for r in result]
 answers.append(dict(id=p.stem,query=p.read_text(),columns=columns,rows=rows))
(D/'query-results.json').write_text(json.dumps(answers,indent=2))
raw=(ROOT/'ontology/mommis-aligned.owl').read_bytes();ontology=parse_ontology(raw);ontology.update(source='Bundled OWL snapshot',status='snapshot')
(D/'ontology.json').write_text(json.dumps(ontology,indent=2));Graph().parse(data=raw,format='xml').serialize(ROOT/'ontology/mommis-aligned.ttl',format='turtle')
html=(ROOT/'explorer/index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','<style>'+(ROOT/'explorer/styles.css').read_text()+'</style>')
payload=dict(data=data,ontology=ontology,queries=answers,rdf=(D/'mvp.ttl').read_text(),owl=raw.decode())
script='window.MOMMIS_BUNDLE='+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+';\n'+(ROOT/'explorer/app.js').read_text()
html=html.replace('<script src="app.js" defer></script>','<script>'+script.replace('</script','<\\/script')+'</script>')
(ROOT/'preview/mommis-mvp-v2.html').write_text(html)
print('Built MVP RDF, four SPARQL result sets, OWL snapshot and offline preview')
