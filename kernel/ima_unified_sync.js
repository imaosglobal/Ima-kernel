const store = {};

function set(user, key, value){
  if(!store[user]) store[user] = {};
  store[user][key] = value;
}

function get(user, key){
  if(!store[user]) return null;
  return store[user][key];
}

function snapshot(user){
  return store[user] || {};
}

module.exports = { set, get, snapshot };
