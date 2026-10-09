import {readFile,writeFile,mkdir} from 'node:fs/promises';
const root=new URL('../',import.meta.url);
const read=p=>readFile(new URL(p,root),'utf8');
const [html,css,app,model,raw]=await Promise.all(['explorer/index.html','explorer/styles.css','explorer/app.mjs','explorer/model.mjs','explorer/data/pilot.json'].map(read));
const data=JSON.parse(raw);
// Standalone download links go to the existing repository PDF rather than a missing sibling file.
for(const source of data.sources)if(source.repositoryPath)source.repositoryPath='https://github.com/Buffalo-Ontology-Group/MOMMIS/blob/main/Literature/msystems.00392-26.pdf';
const script=model.replaceAll('export function','function')+'\n'+app.replace(/^import .*;\n/,'').replace("const response=await fetch('./data/pilot.json');if(!response.ok)throw Error(`Dataset request failed (${response.status})`);\n  data=await response.json();",'data='+JSON.stringify(data).replaceAll('<','\\u003c')+';');
if(script.includes("fetch('./data/pilot.json')"))throw Error('Standalone data replacement failed');
const output=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>').replace('<script type="module" src="app.mjs"></script>','<script type="module">'+script.replaceAll('</script','<\\/script')+'</script>');
await mkdir(new URL('dist/',root),{recursive:true});await writeFile(new URL('dist/mommis-explorer.html',root),output);
console.log('Built dist/mommis-explorer.html; opens without a server or internet connection.');
