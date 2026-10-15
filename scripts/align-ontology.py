"""Build review draft from preserved source files. Requires rdflib."""
from pathlib import Path
import csv,re
from rdflib import Graph,Namespace,URIRef,Literal,RDF,RDFS,OWL,BNode
from rdflib.collection import Collection
root=Path(__file__).resolve().parents[1]; out=root/'ontology'
M=Namespace('http://purl.obolibrary.org/obo/mommis#'); O=Namespace('http://purl.obolibrary.org/obo/'); D=Namespace('http://purl.org/dc/terms/')
old=Graph().parse(out/'legacy/mommis-2025.ttl',format='turtle')
high=Graph().parse(out/'legacy/mommis-high-level.rdf',format='xml')
core=Graph().parse(out/'mommis-milk-core.owl',format='xml')
g=Graph(); review=Graph()
for graph in [g,review]:
 for name,ns in [('mommis',M),('obo',O),('owl',OWL),('rdfs',RDFS),('dct',D)]:graph.bind(name,ns)
ont=URIRef('http://purl.obolibrary.org/obo/mommis')
g.add((ont,RDF.type,OWL.Ontology));g.add((ont,RDFS.label,Literal('MOMMIS aligned review draft')))
g.add((ont,OWL.versionInfo,Literal('0.2.0-review-2026-10-14')))
g.add((ont,D.creator,Literal('Emily Steliotes')))
g.add((ont,D.references,URIRef('https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/2')))
g.add((ont,D.license,URIRef('https://creativecommons.org/licenses/by/4.0/')))
g.add((ont,RDFS.comment,Literal('Review derivative of two user-supplied MOMMIS drafts and the milk-core pattern. Existing MOMMIS namespace reused for continuity, not a claim of registered identifiers. External IRIs are declarations; no full import closure. Review annotations are not accepted biological assertions.')))
for source in ['legacy/mommis-2025.ttl','legacy/mommis-high-level.rdf','mommis-milk-core.owl']:
 g.add((ont,D.source,Literal(source)))
for prop in [D.creator,D.references,D.license,D.source,M.legacyIRI,M.reviewStatus,M.candidateMapping,M.legacyDefinition]:g.add((prop,RDF.type,OWL.AnnotationProperty))
# Keep the new four-class pattern, changing only its temporary local namespace.
prefix='https://example.org/mommis/draft/milk-core/'
def remap(x):return M[str(x)[len(prefix):]] if isinstance(x,URIRef) and str(x).startswith(prefix) else x
for s,p,o in core:
 if s==URIRef(prefix):continue
 g.add(tuple(remap(x) for x in (s,p,o)))
for c in core.subjects(RDF.type,OWL.Class):
 if str(c).startswith(prefix):g.add((remap(c),M.legacyIRI,c))
# Keep all named legacy concepts. Correct only broad category placement here;
# external term matches are candidates until reviewed, not owl:equivalentClass.
parents={
 'BCellActivation':'GO_0008150','CytokineProduction':'GO_0008150',
 'ImmunoglobulinAProduction':'GO_0008150','InnateImmuneResponse':'GO_0008150',
 'Phagocytosis':'GO_0008150','TCellActivation':'GO_0008150','AdaptiveImmuneResponse':'GO_0008150',
 'BioactivePeptide':'CHEBI_16670','HumanMilkOligosaccharides':'CHEBI_50699',
 'GutAssociatedLymphoidTissue':'UBERON_0000479','IntestinalEpithelialCells':'CL_0000000',
 'MilkFatGlobuleMembrane':'BFO_0000040','GutMicrobiotaBalance':None,'ImmuneHealth':None}
candidates={'BCellActivation':'GO_0042113','CytokineProduction':'GO_0001816','InnateImmuneResponse':'GO_0045087','Phagocytosis':'GO_0006909','TCellActivation':'GO_0042110','AdaptiveImmuneResponse':'GO_0002250'}
# Conservative working descriptions; original prose retained separately as annotations.
definitions={
 'BioactivePeptide':'A peptide considered for its biological activity; the criterion and role/disposition pattern remain to be specified.',
 'HumanMilkOligosaccharides':'An oligosaccharide category associated with human milk. Occurrence-based versus structural membership, including synthetic material, remains to be defined.',
 'GutMicrobiotaBalance':'A proposed descriptor of gut microbial community composition or function. Operational definition and upper category unresolved.',
 'ImmuneHealth':'A proposed immune-health concept. Quality, disposition, and outcome interpretations remain unresolved.',
 'MilkFatGlobuleMembrane':'The membrane structure surrounding a milk fat globule. More specific upstream mapping remains to be reviewed.'}
rows=[]
for name,parent in parents.items():
 c=M[name];g.add((c,RDF.type,OWL.Class));g.add((c,RDFS.label,Literal(re.sub(r'(?<!^)(?=[A-Z])',' ',name).lower())))
 g.add((c,M.reviewStatus,Literal('Proposed alignment; Alex Diehl review pending')))
 if parent:g.add((c,RDFS.subClassOf,O[parent]));g.add((O[parent],RDF.type,OWL.Class))
 else:g.add((c,RDFS.comment,Literal('Upper category intentionally unresolved; no function/disposition axiom retained.')))
 if name in definitions:g.add((c,RDFS.comment,Literal(definitions[name])))
 if name in candidates:g.add((c,M.candidateMapping,O[candidates[name]]))
 for source,graph in [('legacy/mommis-2025.ttl',old),('legacy/mommis-high-level.rdf',high)]:
  for oldc in graph.subjects(RDF.type,OWL.Class):
   if str(oldc).rsplit('#',1)[-1].rsplit('HEALTH_',1)[-1]!=name:continue
   g.add((c,M.legacyIRI,oldc));g.add((c,D.source,Literal(source)))
   for p in [RDFS.comment,RDFS.isDefinedBy,O.IAO_0000115]:
    for v in graph.objects(oldc,p):
     if isinstance(v,Literal):g.add((c,M.legacyDefinition,Literal(str(v))))
   rows.append([source,str(oldc),str(c),'Preserved concept; corrected/reviewed category; original prose retained as legacy annotation'])
labels={'GO_0008150':'biological process','CHEBI_16670':'peptide','CHEBI_50699':'oligosaccharide','UBERON_0000479':'tissue','CL_0000000':'cell','BFO_0000040':'material entity'}
for id,label in labels.items():g.add((O[id],RDFS.label,Literal(label)))
# Legacy properties are preserved as review declarations, without unverified alignment.
for source,graph in [('legacy/mommis-2025.ttl',old),('legacy/mommis-high-level.rdf',high)]:
 for prop in graph.subjects(RDF.type,OWL.ObjectProperty):
  if str(prop).startswith(str(O)) and not str(prop).startswith(str(M)):continue
  name=str(prop).split('#')[-1];new=M[name]
  g.add((new,RDF.type,OWL.ObjectProperty));g.add((new,RDFS.label,Literal(re.sub(r'(?<!^)(?=[A-Z])',' ',name).replace('_',' ').lower())))
  g.add((new,M.legacyIRI,prop));g.add((new,M.reviewStatus,Literal('Legacy relation; alignment pending; not used for biological assertions in this draft')))
  rows.append([source,str(prop),str(new),'Relation retained without unverified external subproperty mapping'])
# Preserve all original conceptual relation assertions and axiom annotations as
# annotation-only records outside the OWL module; never copy them as class effects.
props={M.sourceIRI,M.predicateIRI,M.targetIRI,M.reviewStatus,D.source,M.sourceNote}
for p in props:review.add((p,RDF.type,OWL.AnnotationProperty))
items=[]
for source,graph in [('legacy/mommis-2025.ttl',old),('legacy/mommis-high-level.rdf',high)]:
 ops=set(graph.subjects(RDF.type,OWL.ObjectProperty)) | {O.RO_0000086}
 for s,p,o in graph:
  if p in ops and isinstance(s,URIRef) and isinstance(o,URIRef):items.append((source,s,p,o,'Original conceptual assertion; not validated evidence'))
 for ax in graph.subjects(RDF.type,OWL.Axiom):
  s=graph.value(ax,OWL.annotatedSource);p=graph.value(ax,OWL.annotatedProperty);o=graph.value(ax,OWL.annotatedTarget)
  notes='; '.join(str(v) for v in graph.objects(ax,O.IAO_0000119))
  items.append((source,s,p,o,'Unasserted legacy axiom annotation; placeholder citation excluded from evidence: '+notes))
for i,(source,s,p,o,note) in enumerate(sorted(items,key=lambda x:tuple(map(str,x))),1):
 node=M['ReviewLink%03d'%i]
 for pred,obj in [(D.source,Literal(source)),(M.sourceIRI,s),(M.predicateIRI,p),(M.targetIRI,o),(M.reviewStatus,Literal('Unreviewed; NOT an accepted biological assertion')),(M.sourceNote,Literal(note))]:review.add((node,pred,obj))
g.serialize(out/'mommis-aligned.owl',format='xml');g.serialize(out/'mommis-aligned.ttl',format='turtle')
review.serialize(out/'legacy-links-for-review.ttl',format='turtle')
with (out/'legacy-iri-crosswalk.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['source','legacy_iri','aligned_iri','decision']);w.writerows(sorted(rows))
print('Aligned graph:',len(g),'triples;',len(parents)+4,'local classes; review links:',len(items))
