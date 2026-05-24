const fs = require("fs");
const path = require("path");

function applyPatch(text) {
  if (!text) return;

  const blocks = text.split("FILE:").slice(1);

  for (const b of blocks) {
    const [fileLine, ...codeParts] = b.split("CODE:");
    const file = fileLine.trim();
    const code = codeParts.join("CODE:").trim();

    if (!file || !code) continue;

    const full = path.join(process.env.HOME, "ima_kernel", file);

    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, code);

    console.log("[APPLIED]", file);
  }
}

module.exports = { applyPatch };
