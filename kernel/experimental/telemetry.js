
const fs=require('fs');

module.exports=function(event,data){

const row={

time:Date.now(),
event,
data

};

fs.appendFileSync(
'logs/telemetry.log',
JSON.stringify(row)+'\n'
);

};
