import hashlib,json,re,subprocess,unittest
from pathlib import Path
from rdflib import Graph,Namespace,Literal
R=Path(__file__).resolve().parents[1];D=R/'explorer/data';PIN='55097946fe0c3e63f81f8854167e3f1f45382ac6'
class OriginalProvenance(unittest.TestCase):
 def test_every_record_matches_pinned_source(self):
  audit=json.loads((D/'original-selection.json').read_text());d=json.loads((D/'mvp.json').read_text())
  self.assertEqual(audit['sourceCommit'],PIN)
  raw={p:subprocess.check_output(['git','show',PIN+':'+p],cwd=R) for p in audit['sourceFiles']}
  for p,b in raw.items():self.assertEqual(hashlib.sha256(b).hexdigest(),audit['sourceFiles'][p])
  pilot=json.loads(raw['explorer/data/pilot.json']);edges=json.loads(re.search(r'const allEdges = (.*);',raw['explorer/knowledge-graph/source/original.html'].decode())[1]);lookup={e['id']:e for e in edges}
  self.assertEqual(audit['pilotRecords'],pilot['records'])
  self.assertEqual(audit['corpusAssertions'],[lookup[e['id']] for e in audit['corpusAssertions']])
  self.assertEqual(d['glycans'],pilot['glycans']);ids=[]
  for r in d['records']:
   self.assertEqual(r['evidenceOriginCommit'],PIN)
   if r.get('originalAssertion'):
    e=r['originalAssertion'];self.assertEqual(e,lookup[e['id']]);self.assertEqual(r['id'],'C'+str(e['id']).zfill(4));ids.append(e['id'])
    self.assertEqual(r['reviewStatus'],'Imported extraction — unverified')
   else:self.assertEqual(r['originalPilotRecord'],next(x for x in pilot['records'] if x['id']==r['id']))
  self.assertEqual(set(ids),{724,1002,1816,5321,4121,5109,5653})
  self.assertEqual(len({r['id'] for r in d['records']}),10)
 def test_provenance_survives_rdf_export(self):
  g=Graph().parse(D/'mvp.ttl');M=Namespace('https://w3id.org/mommis/mvp/');d=json.loads((D/'mvp.json').read_text())
  for r in d['records']:
   self.assertEqual(str(g.value(M[r['id']],M.originalCommit)),PIN)
   if r.get('originalAssertion'):
    for key in ['evidence','validation_status','quality_score','from','to','label','id']:
     self.assertEqual(g.value(M[r['id']],M['original_'+key]),Literal(r['originalAssertion'][key]))
if __name__=='__main__':unittest.main()
