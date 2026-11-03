"""Structural checks only: not an OWL parser or consistency reasoner."""
from pathlib import Path
import xml.etree.ElementTree as E
n={'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#','rdfs':'http://www.w3.org/2000/01/rdf-schema#','owl':'http://www.w3.org/2002/07/owl#'}
base='https://example.org/mommis/draft/milk-core/'
obo='http://purl.obolibrary.org/obo/'
r=E.parse(Path(__file__).resolve().parents[1]/'ontology/mommis-milk-core.owl').getroot()
about='{'+n['rdf']+'}about';resource='{'+n['rdf']+'}resource'
classes={c.get(about):c for c in r.findall('owl:Class',n)}
expected={'MilkChemicalComponent':('CHEBI_24431',None),'MilkCarbohydrate':('CHEBI_16646','MilkChemicalComponent'),'MilkGlycoprotein':('CHEBI_17089','MilkChemicalComponent'),'MilkAssociated2FL':('CHEBI_147155','MilkCarbohydrate')}
assert len([x for x in classes if x.startswith(base)])==4
for name,(external,parent) in expected.items():
 c=classes[base+name]
 xs=c.find('owl:equivalentClass/owl:Class/owl:intersectionOf',n)
 assert xs is not None and len(xs)==2
 assert xs[0].get(about)==obo+external
 if parent:assert xs[1].get(about)==base+parent
 else:
  assert xs[1].find('owl:onProperty',n).get(resource)==obo+'BFO_0000050'
  assert xs[1].find('owl:someValuesFrom',n).get(resource)==obo+'UBERON_0001913'
 assert all(x.get(resource)!=obo+'UBERON_0001913' for x in c.findall('rdfs:subClassOf',n))
for iri,c in classes.items():
 if iri.startswith(obo):
  assert c.find('owl:equivalentClass',n) is None
  assert c.find('rdfs:subClassOf',n) is None
assert not r.findall('.//owl:sameAs',n)
assert not r.findall('.//owl:imports',n)
print('PASS: XML and four draft class patterns; no generic 2FL milk constraint. OWL reasoning not performed.')
