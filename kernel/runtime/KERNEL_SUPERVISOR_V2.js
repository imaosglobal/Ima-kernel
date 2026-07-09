const { spawn } = require("child_process");

const services = [
  { name: "agent", cmd: "node runtime/KERNEL_BACKGROUND_AGENT_V2.js" },
  { name: "sync", cmd: "node runtime/KERNEL_SYNC_ENGINE.js" }
];

const processes = new Map();

function startService(svc) {
  const p = spawn("sh", ["-c", svc.cmd], {
    stdio: "inherit",
    detached: false
  });

  processes.set(svc.name, p);

  p.on("exit", (code, signal) => {
    console.log(`[SUPERVISOR] ${svc.name} exited`, code, signal);

    setTimeout(() => {
      console.log(`[SUPERVISOR] restarting ${svc.name}`);
      startService(svc);
    }, 2000);
  });

  p.on("error", (err) => {
    console.log(`[SUPERVISOR] error in ${svc.name}`, err.message);
  });

  console.log(`[SUPERVISOR] started ${svc.name}`);
}

function keepAlive() {
  setInterval(() => {
    try {
      const mem = process.memoryUsage();
      if (mem.rss > 500 * 1024 * 1024) {
        console.log("[SUPERVISOR] memory pressure detected");
      }
    } catch {}
  }, 10000);
}

function boot() {
  process.on("uncaughtException", (e) => {
    console.log("[SUPERVISOR CRASH PROTECTED]", e.message);
  });

  process.on("unhandledRejection", (e) => {
    console.log("[SUPERVISOR REJECTION]", e?.message || e);
  });

  console.log("=== KERNEL SUPERVISOR V2 ONLINE ===");

  for (const s of services) startService(s);

  keepAlive();
}

boot();
