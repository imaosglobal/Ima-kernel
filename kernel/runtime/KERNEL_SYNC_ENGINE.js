const fs = require("fs");

function loadState() {
  try {
    return JSON.parse(fs.readFileSync("./runtime/kernel_state.json","utf8"));
  } catch {
    return {};
  }
}

function sync() {
  const state = loadState();
  return {
    local: "1.0.5",
    git: state.version || "unknown",
    npm: "unknown",
    drift: state.snapshot ? false : true
  };
}

function loop() {
  console.log("KERNEL SYNC ENGINE LIVE");

  setInterval(() => {
    try {
      const s = sync();
      fs.writeFileSync(
        "./runtime/sync_state.json",
        JSON.stringify(s, null, 2)
      );
    } catch (e) {
      console.log("[SYNC ERROR]", e.message);
    }
  }, 5000);
}

loop();

module.exports = { sync };
