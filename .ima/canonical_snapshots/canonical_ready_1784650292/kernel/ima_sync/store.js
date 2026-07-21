const fs = require('fs');

const FILE = './ima_state_store.json';

function load(){
  try {
    return JSON.parse(fs.readFileSync(FILE,'utf-8'));
  } catch(e){
    return {};
  }
}

function save(state){
  fs.writeFileSync(FILE, JSON.stringify(state,null,2));
}

let state = load();

module.exports = {
  set(key, value){
    state[key] = value;
    save(state);
    return state;
  },

  get(key){
    return state[key];
  },

  dump(){
    return state;
  }
};
