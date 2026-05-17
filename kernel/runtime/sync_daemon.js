const sync = require("./autonomous_sync");

let running = false;

function startAutoSync(interval = 15000){

  if (running) return;
  running = true;

  console.log("[SYNC DAEMON] started");

  setInterval(()=>{
    const res = sync.cycle();

    console.log("[SYNC]", {
      git: !!res.git.committed,
      push: !!res.push.pushed,
      npm: !!res.npm
    });

  }, interval);
}

module.exports = { startAutoSync };
