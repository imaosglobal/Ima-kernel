
const fs=require('fs');
const cp=require('child_process');

function exec(cmd){

try{

return cp.execSync(
cmd,
{
shell:true,
encoding:'utf8'
}
).toString();

}catch{

return null;

}

}

console.log('AUTONOMOUS RUNTIME ONLINE');

setInterval(()=>{

console.log('HEARTBEAT',Date.now());

exec('node runtime/npm_analytics.js');

exec('git add .');

exec(
'git commit -m "AUTO HEARTBEAT" || true'
);

exec('git push || true');

},1000*60*60);

