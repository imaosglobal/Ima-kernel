
const fs=require('fs');

module.exports=function(event,data){

const row={

time:Date.now(),
event,
data

};

fs.appendFileSync(
'logs/analytics.log',
JSON.stringify(row)+'\n'
);

};
