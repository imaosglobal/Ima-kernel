
const fs=require('fs');

setInterval(()=>{

const row={

time:Date.now(),
event:'self-evolution-check'

};

fs.appendFileSync(
'logs/evolution.log',
JSON.stringify(row)+'\n'
);

},1000*60*30);
