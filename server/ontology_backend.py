"""Read-only OWL-backed API and static explorer. No imports are dereferenced."""
import argparse,hashlib,json,threading,time
from datetime import datetime,timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,quote
from urllib.request import Request,urlopen
from rdflib import Graph,RDF,RDFS,OWL,URIRef,BNode
from rdflib.collection import Collection
ROOT=Path(__file__).resolve().parents[1]
M='http://purl.obolibrary.org/obo/mommis#'
LIMIT=5*1024*1024

def parse_ontology(raw):
    if len(raw)>LIMIT or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Ontology is oversized or contains unsupported XML declarations')
    g=Graph().parse(data=raw,format='xml')
    if not list(g.subjects(RDF.type,OWL.Ontology)):raise ValueError('No owl:Ontology declaration')
    classes=sorted(set(g.subjects(RDF.type,OWL.Class)),key=str)
    if not classes:raise ValueError('No declared OWL classes')
    def label(node):return str(g.value(node,RDFS.label) or node)
    def expression(node,seen=None):
        seen=set() if seen is None else seen
        if node in seen:return '[cyclic expression]'
        if isinstance(node,URIRef):return label(node)
        seen=seen|{node}
        for predicate,joiner in [(OWL.intersectionOf,' AND '),(OWL.unionOf,' OR ')]:
            head=g.value(node,predicate)
            if head is not None:
                items=list(Collection(g,head))
                return '('+joiner.join(expression(x,seen) for x in items)+')'
        prop=g.value(node,OWL.onProperty)
        if prop:
            for pred,word in [(OWL.someValuesFrom,'some'),(OWL.allValuesFrom,'only'),(OWL.hasValue,'value')]:
                value=g.value(node,pred)
                if value is not None:return label(prop)+' '+word+' '+expression(value,seen)
        return '[OWL expression not displayed by this pilot]'
    rows=[]
    for c in classes:
        if isinstance(c,BNode):continue
        rows.append({'iri':str(c),'label':label(c),'local':str(c).startswith(M),
          'parents':[{'iri':str(x) if isinstance(x,URIRef) else None,'label':expression(x)} for x in g.objects(c,RDFS.subClassOf)],
          'equivalentTo':[expression(x) for x in g.objects(c,OWL.equivalentClass)],
          'comments':[str(x) for x in g.objects(c,RDFS.comment)],
          'reviewStatus':[str(x) for x in g.objects(c,URIRef(M+'reviewStatus'))]})
    return {'classes':rows,'version':[str(x) for x in g.objects(None,OWL.versionInfo)],
      'sha256':hashlib.sha256(raw).hexdigest(),'importsFollowed':False,'reasoning':'Asserted OWL structure only; no DL reasoning',
      'generatedAt':datetime.now(timezone.utc).isoformat()}

class OntologyStore:
    def __init__(self,path,github=False,branch='feature/mommis-mvp-v3',interval=30,fetcher=None):
        self.path=Path(path);self.github=github;self.interval=interval;self.next_check=0
        self.url='https://raw.githubusercontent.com/Buffalo-Ontology-Group/MOMMIS/'+quote(branch,safe='/')+'/ontology/mommis-aligned.owl'
        self.fetcher=fetcher or self.fetch_remote;self.lock=threading.Lock();self.value=None;self.raw=None
        try:
            self.raw=self.path.read_bytes();self.value=parse_ontology(self.raw);self.value['source']='Local OWL file'
        except Exception:pass
    def fetch_remote(self):
        with urlopen(Request(self.url,headers={'User-Agent':'MOMMIS-Explorer','Cache-Control':'no-cache'}),timeout=10) as response:
            return response.read(LIMIT+1)
    def get(self):
        with self.lock:
            now=time.monotonic()
            if now>=self.next_check:
                self.next_check=now+self.interval
                try:
                    raw=self.fetcher() if self.github else self.path.read_bytes()
                    value=parse_ontology(raw)
                    value.update(source=self.url if self.github else 'Local OWL file',status='current',checkedAt=datetime.now(timezone.utc).isoformat(),refreshSeconds=self.interval)
                    self.value=value;self.raw=raw
                except Exception as exc:
                    if self.value is None:raise ValueError('No usable ontology: '+str(exc))
                    self.value=dict(self.value,status='stale',error='Update failed; showing last valid ontology: '+str(exc),refreshSeconds=self.interval)
            return dict(self.value)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/ontology.owl':
            try:
                self.server.ontology.get();payload=self.server.ontology.raw;status=200
            except Exception:
                self.send_error(503,'No usable ontology');return
            self.send_response(status);self.send_header('Content-Type','application/rdf+xml');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload);return
        if path=='/api/ontology':
            try:payload=json.dumps(self.server.ontology.get()).encode();status=200
            except Exception as exc:payload=json.dumps({'error':str(exc)}).encode();status=503
            self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload);return
        if path=='/':
            self.send_response(302);self.send_header('Location','/explorer/');self.end_headers();return
        resolved=Path(self.translate_path(self.path)).resolve()
        allowed=[(ROOT/name).resolve() for name in ['explorer','ontology','Literature','preview']]
        if not any(resolved==p or p in resolved.parents for p in allowed):self.send_error(404);return
        super().do_GET()
    def list_directory(self,path):self.send_error(404);return None

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--github',action='store_true');p.add_argument('--branch',default='feature/mommis-mvp-v3');p.add_argument('--port',type=int,default=8000);a=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(Handler,directory=str(ROOT)))
    server.ontology=OntologyStore(ROOT/'ontology/mommis-aligned.owl',github=a.github,branch=a.branch)
    print(f'MOMMIS: http://localhost:{a.port}/explorer/ (GitHub sync: {a.github})',flush=True)
    server.serve_forever()
