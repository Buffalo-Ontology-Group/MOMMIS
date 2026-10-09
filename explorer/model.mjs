export function selectRecords(data, {glycan='all', system='all', query=''}={}) {
  const normalize=s=>s.toLowerCase().replace(/[′’'\s-]/g,'');
  const q=normalize(query);
  return data.records.filter(r=>(glycan==='all'||r.glycanIds.includes(glycan))&&(system==='all'||r.system===system)&&(!q||normalize([r.id,r.title,r.statement,r.strain,r.endpoint,r.exposure,r.system,...r.glycanIds.map(id=>data.glycans.find(g=>g.id===id)?.glytoucan||'')].join(' ')).includes(q)));
}
export function validateData(data) {
  const errors=[];
  for(const key of ['sources','glycans','records']) {
    if(!Array.isArray(data[key])) {errors.push(`${key} must be an array`);continue;}
    const ids=data[key].map(x=>x.id); if(new Set(ids).size!==ids.length)errors.push(`Duplicate ${key} ids`);
  }
  if(errors.length)return errors;
  const sources=new Set(data.sources.map(x=>x.id)), glycans=new Set(data.glycans.map(x=>x.id));
  for(const g of data.glycans){if(!/^G\d{5}[A-Z]{2}$/.test(g.glytoucan))errors.push(`Invalid accession: ${g.id}`);if(!sources.has(g.sourceId))errors.push(`Missing source: ${g.id}`);}
  for(const r of data.records){
    for(const key of ['id','statement','system','exposureType','exposure','strain','comparator','endpoint','sourceLocation','limitation','status'])if(!r[key])errors.push(`${r.id}: missing ${key}`);
    if(!sources.has(r.sourceId))errors.push(`Missing evidence source: ${r.id}`);
    if(!r.glycanIds.length||r.glycanIds.some(id=>!glycans.has(id)))errors.push(`Missing glycan: ${r.id}`);
  }
  return errors;
}
// Study statements remain quoted literal content. No universal biological or causal edges are asserted.
export function toTurtle(data) {
  const lit=s=>JSON.stringify(String(s));
  const lines=['@prefix pilot: <https://example.org/mommis/pilot/> .','@prefix dct: <http://purl.org/dc/terms/> .','@prefix prov: <http://www.w3.org/ns/prov#> .','', '# Prototype namespace only; study records, not an approved MOMMIS ontology.'];
  for(const g of data.glycans) lines.push(`pilot:${g.id} a pilot:GlycanRecord ;\n  dct:title ${lit(g.name)} ;\n  dct:identifier ${lit(g.glytoucan)} ;\n  pilot:wurcs ${lit(g.wurcs)} ;\n  pilot:mappingStatus ${lit(g.mappingStatus)} ;\n  prov:wasDerivedFrom <${data.sources.find(s=>s.id===g.sourceId).url}> .`);
  for(const r of data.records){
    const props=[['dct:identifier',r.id],['dct:description',r.statement],['pilot:system',r.system],['pilot:exposureType',r.exposureType],['pilot:exposure',r.exposure],['pilot:organism',r.organism],['pilot:strain',r.strain],['pilot:model',r.model],['pilot:dose',r.dose],['pilot:duration',r.duration],['pilot:comparator',r.comparator],['pilot:endpoint',r.endpoint],['pilot:sourceLocation',r.sourceLocation],['pilot:limitation',r.limitation],['pilot:status',r.status]];
    lines.push(`pilot:${r.id} a pilot:StudyAssertion ;\n  ${props.map(([p,v])=>p+' '+lit(v)).join(' ;\n  ')} ;\n  pilot:mentionsGlycan ${r.glycanIds.map(id=>'pilot:'+id).join(', ')} ;\n  prov:wasDerivedFrom <${data.sources.find(s=>s.id===r.sourceId).url}> .`);
  }
  return lines.join('\n\n')+'\n';
}
