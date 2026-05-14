const fs = require('fs');

const SNAP_PATH = './runtime/.snapshots.json';

function load(){
  try { return JSON.parse(fs.readFileSync(SNAP_PATH,'utf8')); }
  catch { return []; }
}

function save(s){
  fs.writeFileSync(SNAP_PATH, JSON.stringify(s,null,2));
}

function capture(state){
  const snaps = load();

  snaps.push({
    ts: Date.now(),
    state: JSON.parse(JSON.stringify(state))
  });

  save(snaps);
}

function latest(){
  const snaps = load();
  return snaps[snaps.length - 1];
}

module.exports = { capture, latest };
