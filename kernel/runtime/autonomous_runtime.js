
const fs=require('fs');

setInterval(()=>{

const state={

time:Date.now(),
status:'alive',
memory:process.memoryUsage()

};

fs.writeFileSync(
'logs/heartbeat.json',
JSON.stringify(state,null,2)
);

console.log('IMA HEARTBEAT');

},30000);
