const { spawn } = require("child_process");

const services = [
  {
    name: "agent",
    cmd: "node runtime/KERNEL_BACKGROUND_AGENT_V2.js"
  },
  {
    name: "sync",
    cmd: "node runtime/KERNEL_SYNC_ENGINE.js"
  }
];

const processes = new Map();

function start(svc) {
  const p = spawn("sh", ["-c", svc.cmd], {
    stdio: "inherit"
  });

  processes.set(svc.name, p);

  p.on("exit", () => {
    console.log(`[SUPERVISOR] restart ${svc.name}`);
    setTimeout(() => start(svc), 2000);
  });

  console.log(`[SUPERVISOR] started ${svc.name}`);
}

function boot() {
  console.log("=== KERNEL SUPERVISOR ONLINE ===");

  for (const s of services) {
    start(s);
  }
}

boot();
