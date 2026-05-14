const IMA_GUARD = process.env.IMA_GUARD === "true";
const fs = require("fs");

const state = {
  version: "1.0.0",
  repos: [
    "ima_unified_system",
    "ima_product",
    "ima_npm_package"
  ],
  sync: {
    lastSync: null,
    status: "idle"
  }
};

function syncAll() {
  state.sync.status = "syncing";

  // כאן בעתיד נחבר git submodules / hooks
  if (process.env.DEBUG_SYNC) console.log("SYNC START");
  console.log("repos:", state.repos);

  state.sync.lastSync = Date.now();
  state.sync.status = "done";

  fs.writeFileSync(
    "./ima_master_state.json",
    JSON.stringify(state, null, 2)
  );

  console.log("SYNC COMPLETE");
}

module.exports = { state, syncAll };
if (!IMA_GUARD) { console.log("IMA DISABLED"); process.exit(0); }
