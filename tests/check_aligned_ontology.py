"""RDF round-trip and OWL RL pattern tests; not full DL/import validation."""
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,URIRef
from rdflib.compare import isomorphic
from owlrl import DeductiveClosure,OWLRL_Semantics
root=Path(__file__).resolve().parents[1]/'ontology'
g=Graph().parse(root/'mommis-aligned.owl',format='xml')
t=Graph().parse(root/'mommis-aligned.ttl',format='turtle')
assert isomorphic(g,t),'OWL/XML and Turtle graphs differ'
M=Namespace('http://purl.obolibrary.org/obo/mommis#');O=Namespace('http://purl.obolibrary.org/obo/')
local={s for s in g.subjects(RDF.type,OWL.Class) if str(s).startswith(str(M))}
assert len(local)==18
assert not set(g.subjects(RDF.type,OWL.NamedIndividual))&local
assert (M.HumanMilkOligosaccharides,RDFS.subClassOf,O.CHEBI_50699) in g
assert (M.HumanMilkOligosaccharides,RDFS.subClassOf,O.CHEBI_75771) not in g
assert not list(g.triples((M.BioactivePeptide,None,None)))
assert not list(g.objects(M.ImmuneHealth,RDFS.subClassOf))
assert not list(g.objects(M.GutMicrobiotaBalance,RDFS.subClassOf))
assert len(list(g.triples((None,OWL.imports,None))))==0
for c in [M.MilkChemicalComponent,M.MilkCarbohydrate,M.MilkAssociated2FL]:assert g.value(c,OWL.equivalentClass)
# Deliberately artificial fixtures. Additional chemical types supplied because
# this review draft does not include ChEBI's full upstream hierarchy.
X=Namespace('https://example.org/test-only/')
for x in [X.milkMolecule,X.syntheticMolecule]:
 for cls in [O.CHEBI_147155,O.CHEBI_16646,O.CHEBI_24431]:g.add((x,RDF.type,cls))
g.add((X.sample,RDF.type,O.UBERON_0001913));g.add((X.milkMolecule,O.BFO_0000050,X.sample))
DeductiveClosure(OWLRL_Semantics).expand(g)
assert (X.milkMolecule,RDF.type,M.MilkAssociated2FL) in g
assert (X.syntheticMolecule,RDF.type,M.MilkAssociated2FL) not in g
assert (X.milkMolecule,RDF.type,O.UBERON_0001913) not in g
assert (M.PrebioticDisposition,RDFS.subClassOf,O.BFO_0000016) in g
assert not (M.PrebioticDisposition,RDFS.subClassOf,O.BFO_0000023) in g
print('PASS: equivalent RDF/XML/Turtle graphs, 18 local classes, corrected category guards, and OWL RL context-specific classification with synthetic fixtures.')
print('Full DL consistency and external import closure NOT validated.')
