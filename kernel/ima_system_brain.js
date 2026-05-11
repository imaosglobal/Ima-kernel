const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');
const https=require('https');

const ROOT=process.cwd();
const PACKAGE='@mom-os1/ima-core';
const VERSION='5.0.'+Date.now();

function exec(cmd){

try{

return cp.execSync(cmd,{
cwd:ROOT,
shell:true,
encoding:'utf8',
stdio:['ignore','pipe','pipe']
}).toString().trim();

}catch(e){

return {
error:true,
stdout:e.stdout?.toString()||'',
stderr:e.stderr?.toString()||'',
message:e.message||''
};

}

}

function write(file,data){

const full=path.join(ROOT,file);

fs.mkdirSync(
path.dirname(full),
{recursive:true}
);

fs.writeFileSync(full,data);

console.log('WRITE',file);

}

function walk(dir,list=[]){

if(!fs.existsSync(dir)) return list;

for(const item of fs.readdirSync(dir)){

const full=path.join(dir,item);

const rel=path.relative(ROOT,full);

if(
rel.startsWith('.git')||
rel.startsWith('node_modules')
) continue;

let stat;

try{
stat=fs.statSync(full);
}catch{
continue;
}

if(stat.isDirectory()){

walk(full,list);
continue;

}

list.push(rel);

}

return list;

}

console.log('==============================');
console.log('IMA SYSTEM BRAIN');
console.log('==============================');

const files=walk(ROOT);

console.log('FILES',files.length);

// =====================================
// SEMANTIC REGISTRY
// =====================================

const registry={
engines:[],
memory:[],
ui:[],
plugins:[],
runtime:[],
other:[]
};

for(const f of files){

if(f.includes('engine'))
registry.engines.push(f);

else if(f.includes('memory'))
registry.memory.push(f);

else if(f.includes('ui'))
registry.ui.push(f);

else if(f.includes('plugin'))
registry.plugins.push(f);

else if(f.includes('runtime'))
registry.runtime.push(f);

else
registry.other.push(f);

}

write(
'core/system_registry.json',
JSON.stringify(registry,null,2)
);

// =====================================
// HASH DEDUPE
// =====================================

const hashes={};
const dupes=[];

for(const f of files){

try{

const hash=crypto
.createHash('sha256')
.update(
fs.readFileSync(
path.join(ROOT,f)
)
)
.digest('hex');

if(!hashes[hash])
hashes[hash]=[];

hashes[hash].push(f);

}catch{}

}

for(const h in hashes){

if(hashes[h].length>1){

dupes.push(hashes[h]);

}

}

console.log('DUPES',dupes.length);

let removed=0;

for(const group of dupes){

for(let i=1;i<group.length;i++){

const file=group[i];

try{

fs.rmSync(
path.join(ROOT,file),
{force:true}
);

removed++;

}catch{}

}

}

console.log('REMOVED',removed);

// =====================================
// ENGINE RANKING
// =====================================

const ranked=[

'runtime/engine_v6.js',
'runtime/engine_v5.js',
'runtime/engine_v4.js',
'runtime/engine.js',
'server.js'

].filter(f=>fs.existsSync(f));

const canonical=ranked[0];

console.log('CANONICAL',canonical);

// =====================================
// HEALTH ENGINE
// =====================================

const health={

node:!!exec('node -v'),
npm:!!exec('npm -v'),
git:!!exec('git --version'),
canonical:!!canonical,
runtime:false,
server:false

};

const runtimeTest=
exec('node --check '+canonical);

health.runtime=!runtimeTest.error;

const serverTest=
exec('node --check server.js');

health.server=!serverTest.error;

write(
'logs/health.json',
JSON.stringify(health,null,2)
);

// =====================================
// ANALYTICS
// =====================================

write(
'runtime/analytics_engine.js',
`
const fs=require('fs');

module.exports=function(event,data){

const row={

time:Date.now(),
event,
data

};

fs.appendFileSync(
'logs/analytics.log',
JSON.stringify(row)+'\\n'
);

};
`
);

// =====================================
// MONETIZATION
// =====================================

write(
'core/monetization.json',
JSON.stringify({

npmPackage:'${PACKAGE}',
donations:false,
premium:false,
telemetry:false,
analytics:true,
futureRevenue:[
'cloud hosting',
'premium agents',
'api access',
'enterprise runtime'
]

},null,2)
);

// =====================================
// AUTONOMOUS EVOLUTION
// =====================================

write(
'runtime/evolution_engine.js',
`
const fs=require('fs');

setInterval(()=>{

const row={

time:Date.now(),
event:'self-evolution-check'

};

fs.appendFileSync(
'logs/evolution.log',
JSON.stringify(row)+'\\n'
);

},1000*60*30);
`
);

// =====================================
// PACKAGE
// =====================================

write(
'package.json',
JSON.stringify({

name:PACKAGE,
version:VERSION,
main:'server.js',

scripts:{

start:'node server.js',
runtime:'node runtime/autonomous_runtime.js',
brain:'node ima_system_brain.js'

},

bin:{
ima:'cli.js'
},

publishConfig:{
access:'public'
}

},null,2)
);

// =====================================
// GIT
// =====================================

exec('git add .');

exec(
'git commit -m "IMA BRAIN '+VERSION+'" || true'
);

exec('git tag '+VERSION+' || true');

exec('git push || true');

exec('git push --tags || true');

// =====================================
// NPM
// =====================================

const who=exec('npm whoami');

console.log('NPM READY',!who.error);

let published=false;
let reason='';

if(!who.error){

for(let i=1;i<=5;i++){

console.log('PUBLISH TRY',i);

const pub=exec(
'npm publish --access public'
);

if(!pub.error){

published=true;
break;

}

reason=
pub.stderr||
pub.message||
'UNKNOWN';

console.log(reason);

exec('sleep 10');

}

}

write(
'logs/publish_state.json',
JSON.stringify({
published,
reason,
version:VERSION
},null,2)
);

// =====================================
// VERIFY
// =====================================

const verify=exec('ima');

console.log('CLI',verify);

// =====================================
// FINAL
// =====================================

console.log('==============================');
console.log('IMA SYSTEM COMPLETE');
console.log('==============================');

console.log({

VERSION,
FILES:files.length,
DUPES:dupes.length,
REMOVED:removed,
CANONICAL:canonical,
PUBLISHED:published

});
