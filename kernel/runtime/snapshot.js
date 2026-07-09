const fs = require("fs");

const SNAP = "./kernel/sync_snapshot.json";

function saveSnapshot(){
  const data = {
    ts: Date.now()
  };
  fs.writeFileSync(SNAP, JSON.stringify(data, null, 2));
  return { ok:true, saved:true };
}

module.exports = { saveSnapshot };
