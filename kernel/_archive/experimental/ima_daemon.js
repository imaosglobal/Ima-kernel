const { spawn } = require("child_process");
const { execSync } = require("child_process");

const KERNEL = __dirname + "/ima_saas_full.js";
const FIREWALL = __dirname + "/kernel_firewall.js";

function startFirewall() {
  spawn("node", [FIREWALL], {
    stdio: "inherit"
  });
}

function startKernel() {
  console.log("[DAEMON] starting kernel...");

  const child = spawn("node", [KERNEL], {
    stdio: "inherit"
  });

  child.on("exit", () => {
    setTimeout(startKernel, 2000);
  });
}

startFirewall();
startKernel();
