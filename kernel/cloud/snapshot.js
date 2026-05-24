const fs = require("fs");
const path = require("path");

function readTree(dir, out = []) {
  const files = fs.readdirSync(dir);

  for (const f of files) {
    const full = path.join(dir, f);

    try {
      const stat = fs.statSync(full);

      if (stat.isDirectory()) {
        if (f === "node_modules" || f.startsWith(".")) continue;
        readTree(full, out);
      } else {
        const content = fs.readFileSync(full, "utf8").slice(0, 4000);
        out.push({
          file: full.replace(process.env.HOME + "/ima_kernel/", ""),
          content
        });
      }
    } catch (e) {}
  }

  return out;
}

function buildSnapshot() {
  const root = path.join(process.env.HOME, "ima_kernel");

  const data = {
    time: new Date().toISOString(),
    files: readTree(root)
  };

  return JSON.stringify(data, null, 2);
}

module.exports = { buildSnapshot };
