import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {selectRecords,toTurtle,validateData,toReviewCsv} from '../explorer/model.mjs';
const data=JSON.parse(await readFile(new URL('../explorer/data/pilot.json',import.meta.url),'utf8'));
test('all evidence has provenance and experimental context',()=>assert.deepEqual(validateData(data),[]));
test('identifier-only 3-FL does not acquire 2-FL evidence',()=>assert.equal(selectRecords(data,{glycan:'3fl'}).length,0));
test('animal mixture retains comparator and is not a human claim',()=>{const [r]=selectRecords(data,{system:'Animal'});assert.equal(r.id,'E003');assert.equal(r.exposureType,'Mixture + microbe');assert.match(r.comparator,/without B. infantis/);assert.match(r.limitation,/does not isolate/);assert.equal(selectRecords(data,{system:'Human'}).length,0);});
test('search finds accession and strain without changing evidence identity',()=>{assert.equal(selectRecords(data,{query:'G49708ZB'}).length,3);assert.deepEqual(selectRecords(data,{query:'Bi-26'}).map(r=>r.id),['E001','E002']);assert.equal(selectRecords(data,{query:"2'-FL"}).length,3);});
test('counts distinguish records from independent studies',()=>assert.equal(new Set(data.records.map(r=>r.sourceId)).size,2));
test('RDF preserves contextual statements and escapes literal content',()=>{const copy=structuredClone(data);copy.records[0].statement='A "quoted" statement\nwith a new line';const ttl=toTurtle(copy);assert.match(ttl,/\\"quoted\\"/);assert.match(ttl,/pilot:comparator/);assert.match(ttl,/pilot:exposureType "Mixture \+ microbe"/);assert.equal((ttl.match(/a pilot:StudyAssertion/g)||[]).length,3);assert.doesNotMatch(ttl,/owl:sameAs|pilot:causes|pilot:treats/);});
test('invalid source and duplicate ids are rejected',()=>{const copy=structuredClone(data);copy.records[0].sourceId='absent';assert.match(validateData(copy).join(),/Missing evidence source/);copy.glycans.push(copy.glycans[0]);assert.match(validateData(copy).join(),/Duplicate/);});

test('search resolves molecular names, MilkOligoDB IDs, and study citations',()=>{
  const g=data.glycans.find(g=>g.id==='2fl');
  for(const query of [g.name,g.milkOligoId])assert.equal(selectRecords(data,{query}).length,3);
  assert.equal(selectRecords(data,{query:'Zabel'}).length,2);
  assert.equal(selectRecords(data,{query:data.glycans.find(g=>g.id==='3fl').milkOligoId}).length,0);
});
test('review CSV respects filters and preserves mixture context and scientific status',()=>{
  const csv=toReviewCsv(data,{system:'Animal'},{E003:{state:'Ready for domain review',note:'Check Figure 2'}});
  assert.match(csv,/E003/);assert.doesNotMatch(csv,/E001|E002/);
  for(const value of [data.records[2].comparator,data.records[2].limitation,data.records[2].status,'Check Figure 2'])assert.ok(csv.includes(value.replaceAll('"','""')));
  assert.equal(toReviewCsv(data,{system:'Human'}).split('\r\n').length,2);
});
test('review CSV quotes multiline notes and neutralizes spreadsheet formulas',()=>{
  const csv=toReviewCsv(data,{query:'E001'},{E001:{note:'=SUM(1,2)\n"check"'}});
  assert.ok(csv.includes('"\'=SUM(1,2)\n""check"""'));
  assert.equal(data.records[0].id,'E001');
});
