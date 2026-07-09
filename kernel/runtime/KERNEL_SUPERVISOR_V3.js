const { spawn } = require("child_process");

function start(name, cmd) {
  function run() {
    console.log(`[SUPERVISOR] starting ${name}`);

    const p = spawn("sh", ["-c", cmd], {
      stdio: "ignore",
      detached: true
    });

    p.unref();

    p.on("exit", () => {
      console.log(`[SUPERVISOR] restart ${name}`);
      setTimeout(run, 3000);
    });
  }

  run();
}

function boot() {
  console.log("=== SUPERVISOR V3 (STABLE MODE) ===");

  process.on("uncaughtException", (e) => {
    console.log("[SUPERVISOR SAFE]", e.message);
  });

  start("agent", "node runtime/KERNEL_BACKGROUND_AGENT_V2.js");
  start("sync", "node runtime/KERNEL_SYNC_ENGINE.js");
}

boot();
