const { execSync } = require("child_process");
const fs = require("fs");

const policy = JSON.parse(
  fs.readFileSync(__dirname + "/kernel_policy.json", "utf8")
);

function enforce() {
  try {
    const out = execSync("pgrep -a node || true")
      .toString()
      .split("\n")
      .filter(Boolean);

    out.forEach(line => {
      const pid = line.split(" ")[0];
      const cmd = line;

      const allowed = policy.allowed_processes.some(p =>
        cmd.includes(p)
      );

      const forbidden = policy.forbidden_patterns.some(p =>
        new RegExp(p).test(cmd)
      );

      if (!allowed || forbidden) {
        try {
          console.log("[KERNEL POLICY KILL]", cmd);
          process.kill(parseInt(pid), "SIGKILL");
        } catch {}
      }
    });

  } catch (e) {
    console.log("[ENFORCER ERROR]", e.message);
  }
}

module.exports = { enforce };
