const fs = require("fs");
const { execSync } = require("child_process");

function score() {
  try {
    const out = execSync(
      "curl -s http://localhost:4000/ima/run -X POST -H 'Content-Type: application/json' -d '{\"message\":\"expand\"}'"
    ).toString();
    const parsed = JSON.parse(out);
    return parsed.debug?.score || 50;
  } catch {
    return 50;
  }
}

function maybeExtend() {
  const base = score();

  // 🧠 stronger exploration pressure
  const s = base + (Math.random() * 8 - 2);

  console.log("🧠 EXTENSION SCORE:", s.toFixed(2));

  // 🧠 relaxed threshold for emergence
  if (s > 48) {
    const moduleName = `auto_module_${Date.now()}.js`;

    const code = `
module.exports = {
  name: "${moduleName}",
  created: ${Date.now()},
  behavior: "auto-generated capability layer",
  execute: () => {
    return "Ima extended module active";
  }
};
`;

    const path = `./ima_runtime/${moduleName}`;
    fs.writeFileSync(path, code);

    console.log("🚀 NEW MODULE CREATED:", moduleName);

    try {
      execSync("git add .");
      execSync(`git commit -m "self-extension ${moduleName}"`);
      execSync("git push");
      console.log("📦 EXTENSION COMMITTED");
    } catch (e) {
      console.log("⚠️ git error:", e.message);
    }

  } else {
    console.log("🧠 SYSTEM NOT READY (exploration ongoing)");
  }
}

maybeExtend();
