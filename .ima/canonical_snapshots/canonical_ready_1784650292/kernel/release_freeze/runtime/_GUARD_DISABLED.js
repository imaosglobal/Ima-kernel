const { execSync } = require("child_process");

function killDuplicates() {
  const out = execSync("pgrep -af autonomous_runtime.js").toString();
  const lines = out.split("\n").filter(Boolean);

  if (lines.length > 1) {
    // רק kill, לא restart (מניע כפילויות אינסופיות)
    execSync("pkill -f autonomous_runtime.js");
  }
}

setInterval(killDuplicates, 3000);
