
const fs = require('fs');

let logs = [];

function save(cmd, plan){
  logs.push({cmd, plan, t:Date.now()});
  fs.writeFileSync('./ima_memory.json', JSON.stringify(logs, null, 2));
}

function get(){
  return logs;
}

module.exports = { save, get };
