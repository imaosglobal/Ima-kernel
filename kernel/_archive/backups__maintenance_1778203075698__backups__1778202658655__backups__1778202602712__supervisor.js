const { execSync } = require("child_process");

function enforceSingleKernel() {
  console.log("[SUPERVISOR] enforcing single kernel...");

  const targets = [
    "server.js",
    "ima_unified_system",
    "ima_saas_full.js"
  ];

  targets.forEach(t => {
    try {
      execSync(`pkill -f "${t}" || true`);
    } catch {}
  });

  console.log("[SUPERVISOR] cleanup done");
}

module.exports = { enforceSingleKernel };
