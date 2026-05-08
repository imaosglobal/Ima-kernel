const { execSync } = require("child_process");

const ALLOWED = [
  "ima_daemon.js",
  "ima_saas_full.js"
];

function scanAndEnforce() {
  try {
    const out = execSync("pgrep -a node || true")
      .toString()
      .split("\n")
      .filter(Boolean);

    out.forEach(line => {
      const pid = line.split(" ")[0];
      const cmd = line;

      const isAllowed = ALLOWED.some(a => cmd.includes(a));

      if (!isAllowed) {
        console.log("[FIREWALL KILL]", cmd);
        try {
          process.kill(parseInt(pid), "SIGKILL");
        } catch {}
      }
    });

  } catch (e) {
    console.log("[FIREWALL ERROR]", e.message);
  }
}

// 🔁 continuous enforcement loop
setInterval(scanAndEnforce, 3000);

console.log("=== KERNEL FIREWALL ACTIVE ===");
scanAndEnforce();
