import {readFile,writeFile} from 'node:fs/promises';
import {toTurtle,validateData} from '../explorer/model.mjs';
const data=JSON.parse(await readFile(new URL('../explorer/data/pilot.json',import.meta.url),'utf8'));
const errors=validateData(data);if(errors.length)throw Error(errors.join('\n'));
await writeFile(new URL('../explorer/data/pilot.ttl',import.meta.url),toTurtle(data));
console.log(`Exported ${data.glycans.length} glycan records and ${data.records.length} study assertions.`);
