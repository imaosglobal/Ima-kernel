const fs = require('fs');

const DB = './ima_devices.json';

function load(){
  if(!fs.existsSync(DB)) return {};
  return JSON.parse(fs.readFileSync(DB,'utf8'));
}

function save(d){
  fs.writeFileSync(DB, JSON.stringify(d,null,2));
}

function register(user, device){
  const db = load();

  if(!db[user]) db[user] = { devices: [], last: null };

  if(!db[user].devices.includes(device)){
    db[user].devices.push(device);
  }

  db[user].last = device;

  save(db);
  return db[user];
}

function list(user){
  const db = load();
  return db[user] || { devices: [] };
}

function switchDevice(user, device){
  return register(user, device);
}

module.exports = { register, list, switchDevice };
