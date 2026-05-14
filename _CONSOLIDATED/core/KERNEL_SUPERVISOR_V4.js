const { spawn } = require("child_process");

function run(name, cmd) {
  console.log(`[SUPERVISOR] boot ${name}`);

  const start = () => {
    const p = spawn("sh", ["-c", cmd], {
      stdio: "inherit"
    });

    p.on("exit", (code) => {
      console.log(`[SUPERVISOR] ${name} exited:`, code);
      setTimeout(start, 2000);
    });

    p.on("error", (e) => {
      console.log(`[SUPERVISOR] ${name} error:`, e.message);
      setTimeout(start, 3000);
    });
  };

  start();
}

function boot() {
  console.log("=== SUPERVISOR V4 (HARD STABLE MODE) ===");

  process.on("uncaughtException", e => {
    console.log("[SUPERVISOR SAFE]", e.message);
  });

  run("agent", "node runtime/KERNEL_BACKGROUND_AGENT_V2.js");
  run("sync", "node runtime/KERNEL_SYNC_ENGINE.js");
}

boot();
