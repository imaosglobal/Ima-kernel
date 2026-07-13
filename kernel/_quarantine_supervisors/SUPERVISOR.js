const { spawn } = require("child_process");
const state = require("./KERNEL_STATE").state;

const TARGET = require("path").resolve(__dirname, "autonomous_runtime.js");

let child = null;

function start() {
  child = spawn("node", [TARGET], {
    stdio: ["ignore", "pipe", "pipe"]
  });

  child.stdout.on("data", (d) => {
    const msg = d.toString().trim();
    console.log(msg);

    if (msg.includes("HEARTBEAT")) {
      state.lastHeartbeat = Date.now();
      state.runtime = "alive";
    }
  });

  child.on("exit", (code) => {
    console.log("RUNTIME EXIT:", code);
    state.runtime = "dead";
    setTimeout(start, 1000);
  });
}

setInterval(() => {
  const diff = Date.now() - (state.lastHeartbeat || 0);

  if (diff > 8000) {
    console.log("KERNEL STATE: STALL DETECTED");
    if (child) child.kill("SIGKILL");
  }
}, 3000);

console.log("SUPERVISOR ONLINE");
start();
