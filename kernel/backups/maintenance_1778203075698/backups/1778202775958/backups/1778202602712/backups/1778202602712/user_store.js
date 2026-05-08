const fs = require("fs");

const FILE = "users.json";

function load(){
  try { return JSON.parse(fs.readFileSync(FILE)); }
  catch { return {}; }
}

function save(data){
  fs.writeFileSync(FILE, JSON.stringify(data,null,2));
}

function getUser(apiKey){
  const db = load();
  return db[apiKey];
}

function createUser(apiKey){
  const db = load();
  db[apiKey] = { plan: "free", usage: 0 };
  save(db);
}

function upgradeUser(apiKey){
  const db = load();
  if(db[apiKey]){
    db[apiKey].plan = "pro";
    save(db);
  }
}

function increment(apiKey){
  const db = load();
  if(!db[apiKey]) return null;

  const limit = db[apiKey].plan === "free" ? 2 : 100000;

  if(db[apiKey].usage >= limit){
    return "PAY";
  }

  db[apiKey].usage++;
  save(db);

  return null;
}

module.exports = { getUser, createUser, upgradeUser, increment };
