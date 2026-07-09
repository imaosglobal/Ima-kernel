
const fs = require('fs');
const FILE = './ima_long_memory.json';

function load(){
  try { return JSON.parse(fs.readFileSync(FILE)); }
  catch(e){ return []; }
}

function save(entry){
  const data = load();
  data.push(entry);
  fs.writeFileSync(FILE, JSON.stringify(data,null,2));
}

function last(n=10){
  const data = load();
  return data.slice(-n);
}

module.exports = { load, save, last };
