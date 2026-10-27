import json,unittest
from pathlib import Path
from rdflib import Graph,RDF,RDFS,OWL,Namespace,URIRef
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'explorer/data';M=Namespace('https://w3id.org/mommis/mvp/')
class MVPTests(unittest.TestCase):
 def test_scope_and_provenance(self):
  d=json.loads((D/'mvp.json').read_text());self.assertEqual(len(d['records']),12);self.assertEqual(len(d['entities']),18)
  ids={n['id'] for n in d['entities']};src={s['id'] for s in d['sources']}
  for r in d['records']:
   self.assertIn(r['subject'],ids);self.assertIn(r['target'],ids);self.assertIn(r['sourceId'],src)
   for k in ['comparator','model','exposure','reviewStatus','origin','limitation']:self.assertTrue(r[k])
  self.assertEqual(len({r['sourceId'] for r in d['records']}),7)
  self.assertFalse(any('3fl' in r['glycanIds'] for r in d['records']))
 def test_queries_and_reification(self):
  g=Graph().parse(D/'mvp.ttl');self.assertEqual(len(list(g.subjects(RDF.type,M.EvidenceAssertion))),12)
  self.assertFalse(list(g.triples((None,M.reportsEndpoint,None))))
  expected=[2,8,12,11]
  for path,count in zip(sorted((ROOT/'queries').glob('*.rq')),expected):self.assertEqual(len(list(g.query(path.read_text()))),count,path.name)
 def test_owl_isomorphic_and_scope(self):
  from rdflib.compare import isomorphic
  g=Graph().parse(ROOT/'ontology/mommis-aligned.owl');t=Graph().parse(ROOT/'ontology/mommis-aligned.ttl');self.assertTrue(isomorphic(g,t))
  self.assertEqual(len([c for c in g.subjects(RDF.type,OWL.Class) if str(c).startswith('http://purl.obolibrary.org/obo/mommis#')]),18)
  self.assertFalse(list(g.triples((URIRef('http://purl.obolibrary.org/obo/mommis#BioactivePeptide'),None,None))))
  self.assertTrue(list(g.triples((URIRef('http://purl.obolibrary.org/obo/mommis#PrebioticDisposition'),None,None))))
if __name__=='__main__':unittest.main()
