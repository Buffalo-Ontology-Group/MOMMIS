import {selectRecords,validateData,toTurtle} from './model.mjs';
const $=id=>document.getElementById(id);
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const key='mommis-pilot-reviews-v1';
let data,selected=null,reviews={},storageAvailable=true;
try {const raw=JSON.parse(localStorage.getItem(key)||'{}');if(raw&&typeof raw==='object'&&!Array.isArray(raw))reviews=raw;}catch{storageAvailable=false;}
function toast(message){$('toast').textContent=message;$('toast').style.display='block';clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('toast').style.display='none',3500);}
function source(id){return data.sources.find(s=>s.id===id);}
function showView(view){for(const name of ['evidence','molecules','sources'])$(name+'-view').hidden=name!==view;for(const b of document.querySelectorAll('[data-view]')){b.classList.toggle('active',b.dataset.view===view);if(b.dataset.view===view)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');}}
function filters(){return {query:$('search').value,glycan:$('glycan').value,system:$('system').value};}
function render(){
  const records=selectRecords(data,filters());
  if(!records.some(r=>r.id===selected))selected=records[0]?.id||null;
  $('count').textContent=`${records.length} evidence record${records.length===1?'':'s'} · ${new Set(records.map(r=>r.sourceId)).size} distinct studies · all seed records await domain review`;
  $('records').innerHTML=records.length?records.map(r=>`<button class="record" data-id="${r.id}" aria-pressed="${r.id===selected}"><div class="tags"><span class="tag ${r.system==='Animal'?'animal':''}">${escape(r.system)}</span><span class="tag">${escape(r.exposureType)}</span><span class="record-id">${r.id}</span></div><h2>${escape(r.title)}</h2><p>${escape(r.strain)} · ${escape(r.stage)}</p><small>${escape(source(r.sourceId).citation)}</small></button>`).join(''):`<div class="empty"><h2>No records in this pilot view</h2><p>${$('system').value==='Human'?'No human studies have been curated into this prototype.':$('glycan').value==='3fl'?'3-FL has an identifier record, but no curated biological evidence yet.':'Try clearing the search or filters.'}</p><p>This is a coverage gap in this dataset, not evidence that the relationship is absent.</p></div>`;
  for(const b of $('records').querySelectorAll('button'))b.onclick=()=>{selected=b.dataset.id;render();};
  renderDetail();
}
function renderDetail(){
  const r=data.records.find(x=>x.id===selected);
  if(!r){$('detail').innerHTML='<h2>Evidence stays contextual</h2><p>Select another filter to inspect a study record. Each record preserves its exposure, comparator and experimental system.</p>';return;}
  const s=source(r.sourceId), note=reviews[r.id]||{};
  const fields=[['Exposure',r.exposure],['Strain',r.strain],['Experimental system',r.model],['Comparator',r.comparator],['Dose',r.dose],['Duration',r.duration]];
  $('detail').innerHTML=`<div class="tags"><span class="tag draft">${escape(r.status)}</span><span class="record-id">${r.id}</span></div><h2>${escape(r.title)}</h2><p class="statement">${escape(r.statement)}</p><div class="relation" aria-label="Study exposure and measured endpoint"><span>${escape(r.exposure)}</span><b>studied for →</b><span>${escape(r.endpoint)}</span></div><dl class="context">${fields.map(([k,v])=>`<div><dt>${k}</dt><dd>${escape(v)}</dd></div>`).join('')}</dl><section class="evidence-box"><h3>Trace the evidence</h3><a href="${escape(s.url)}" target="_blank" rel="noopener noreferrer">${escape(s.citation)} ↗</a><p><strong>Location:</strong> ${escape(r.sourceLocation)}</p><p>${escape(r.evidenceSummary)}</p>${s.repositoryPath?`<a href="${s.repositoryPath}" target="_blank" rel="noopener">Open repository PDF ↗</a>`:''}</section><div class="limitation"><strong>Interpretation boundary</strong><br>${escape(r.limitation)}</div><section class="review"><h3>Curation workspace</h3><p class="next-action">${escape(r.nextAction)}</p><label>Personal review state<select id="review-state"><option>Not reviewed</option><option>In progress</option><option>Ready for domain review</option></select></label><label>Notes<textarea id="review-note" placeholder="Record missing context, a figure check, or a proposed ontology mapping…"></textarea></label><div class="review-actions"><span>Personal notes do not approve the scientific assertion.</span><button id="save-note">Save note</button></div></section>`;
  if(['Not reviewed','In progress','Ready for domain review'].includes(note.state))$('review-state').value=note.state;
  $('review-note').value=typeof note.note==='string'?note.note:'';
  $('review-note').oninput=()=>{rememberNote(r.id,false);};
  $('review-state').onchange=()=>{rememberNote(r.id,false);};
  $('save-note').onclick=()=>rememberNote(r.id,true);
}
function rememberNote(id,notify){
  reviews[id]={state:$('review-state').value,note:$('review-note').value,updatedAt:new Date().toISOString()};
  try{localStorage.setItem(key,JSON.stringify(reviews));storageAvailable=true;}catch{storageAvailable=false;}
  $('storage-state').textContent=storageAvailable?'Notes stay in this browser; export to keep a portable copy.':'Browser storage unavailable. Notes last for this session only; export before leaving.';
  if(notify)toast(storageAvailable?'Note saved in this browser.':'Note kept for this session; export a copy.');
}
function renderMolecules(){
  $('molecules').innerHTML=data.glycans.map(g=>`<article class="molecule"><div class="row"><div><p class="eyebrow">GLYCAN IDENTITY</p><h3>${escape(g.label)} <small>· ${escape(g.name)}</small></h3></div><button data-glycan="${g.id}">Explore evidence (${data.records.filter(r=>r.glycanIds.includes(g.id)).length})</button></div><p>${escape(g.structure)}</p><div class="source-links"><a href="https://glytoucan.org/Structures/Glycans/${g.glytoucan}" target="_blank" rel="noopener">${g.glytoucan} ↗</a><a href="${escape(source(g.sourceId).url)}" target="_blank" rel="noopener">Project mapping ↗</a></div><p>MilkOligoDB record: ${escape(g.milkOligoId)} · ${escape(g.sourceLocation)}</p><code>${escape(g.wurcs)}</code><p>${escape(g.mappingStatus)}</p></article>`).join('');
  for(const b of document.querySelectorAll('[data-glycan]'))b.onclick=()=>{$('glycan').value=b.dataset.glycan;$('system').value='all';$('search').value='';showView('evidence');render();};
}
function renderSources(){
  $('sources').innerHTML=data.sources.map(s=>`<article class="source"><span class="tag">${escape(s.kind)}</span><h3>${escape(s.title)}</h3><p>${escape(s.citation)}</p><p>${escape(s.role)}</p><div class="source-links"><a href="${escape(s.url)}" target="_blank" rel="noopener">Open source ↗</a>${s.repositoryPath?`<a href="${s.repositoryPath}" target="_blank" rel="noopener">Repository PDF ↗</a>`:''}</div></article>`).join('');
}
function download(name,text,type){const url=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
try {
  const response=await fetch('./data/pilot.json');if(!response.ok)throw Error(`Dataset request failed (${response.status})`);
  data=await response.json();const errors=validateData(data);if(errors.length)throw Error(errors.join('; '));
  for(const g of data.glycans){const option=document.createElement('option');option.value=g.id;option.textContent=g.label;$('glycan').append(option);}
  for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>showView(b.dataset.view);
  for(const id of ['search','glycan','system'])$(id).addEventListener(id==='search'?'input':'change',render);
  $('clear').onclick=()=>{$('search').value='';$('glycan').value='all';$('system').value='all';render();};
  for(const b of document.querySelectorAll('[data-question]'))b.onclick=()=>{if(b.dataset.question==='sources'){showView('sources');return;}$('search').value=b.dataset.question==='utilization'?'growth':'Th17';$('glycan').value='all';$('system').value='all';render();};
  $('export-json').disabled=$('export-rdf').disabled=false;
  $('export-json').onclick=()=>{download('mommis-pilot-with-notes.json',JSON.stringify({...data,personalReviews:reviews},null,2),'application/json');toast('Exported the complete dataset and personal notes.');};
  $('export-rdf').onclick=()=>{download('mommis-pilot.ttl',toTurtle(data),'text/turtle');toast('Exported study records. Personal notes are in the JSON export.');};
  if(!storageAvailable)$('storage-state').textContent='Browser storage unavailable. Export notes before leaving.';
  render();renderMolecules();renderSources();
}catch(error){$('count').textContent='The pilot could not be loaded.';$('records').innerHTML='<div class="empty"><h2>Start the local web server</h2><p>From the repository root, run <code>python3 -m http.server 8000</code> and open http://localhost:8000/explorer/.</p></div>';$('detail').textContent=error.message;}
