const { execSync } = require("child_process");

function getChanges() {
  const output = execSync("git status --porcelain").toString().trim();
  if (!output) return [];

  return output.split("\n").map(line => {
    const status = line.slice(0, 2).trim();
    const file = line.slice(3).trim();
    return { status, file };
  });
}

function classify(changes) {
  let type = "minor";

  for (const c of changes) {
    if (c.file.includes("server") || c.file.includes("kernel")) {
      type = "core";
    }
    if (c.file.includes("memory") || c.file.includes("engine")) {
      type = "logic";
    }
    if (c.file.includes(".md")) {
      type = "docs";
    }
  }

  return type;
}

module.exports = { getChanges, classify };
