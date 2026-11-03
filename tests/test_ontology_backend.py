import sys,tempfile,unittest,json,threading
from pathlib import Path
from functools import partial
from urllib.request import urlopen
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'server'))
from ontology_backend import parse_ontology,OntologyStore,Handler,ThreadingHTTPServer
RAW=(root/'ontology/mommis-aligned.owl').read_bytes()
class OntologyBackendTests(unittest.TestCase):
 def test_reads_real_axioms(self):
  data=parse_ontology(RAW);self.assertEqual(sum(c['local'] for c in data['classes']),18)
  c=next(c for c in data['classes'] if c['iri'].endswith('#MilkChemicalComponent'))
  self.assertIn('part of some milk',c['equivalentTo'][0])
 def test_local_edit_updates_without_restart(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.owl';p.write_bytes(RAW);s=OntologyStore(p,interval=0);before=s.get()
   p.write_bytes(RAW.replace(b'milk carbohydrate',b'reviewed milk carbohydrate'))
   after=s.get();self.assertNotEqual(before['sha256'],after['sha256'])
   self.assertTrue(any(c['label']=='reviewed milk carbohydrate' for c in after['classes']))
 def test_remote_edit_and_invalid_fallback(self):
  values=iter([RAW,RAW.replace(b'milk carbohydrate',b'updated carbohydrate'),b'broken xml'])
  s=OntologyStore(root/'ontology/mommis-aligned.owl',github=True,interval=0,fetcher=lambda:next(values))
  first=s.get();second=s.get();bad=s.get()
  self.assertNotEqual(first['sha256'],second['sha256']);self.assertEqual(bad['sha256'],second['sha256']);self.assertEqual(bad['status'],'stale')
 def test_rejects_entity_declarations(self):
  with self.assertRaises(ValueError):parse_ontology(b'<!DOCTYPE foo><rdf/>')
 def test_api_serves_ontology(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
  server.ontology=OntologyStore(root/'ontology/mommis-aligned.owl',interval=0)
  worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
  try:
   with urlopen(f'http://127.0.0.1:{server.server_port}/api/ontology') as response:
    value=json.load(response);self.assertEqual(value['status'],'current');self.assertIn('classes',value)
   with urlopen(f'http://127.0.0.1:{server.server_port}/api/ontology.owl') as response:
    self.assertEqual(response.read(),RAW)
  finally:server.shutdown();server.server_close();worker.join()
if __name__=='__main__':unittest.main()
