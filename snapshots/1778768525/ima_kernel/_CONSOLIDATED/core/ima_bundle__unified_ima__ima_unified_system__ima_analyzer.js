const fs = require("fs");

function analyze() {
  const code = fs.readFileSync("server.js", "utf-8");

  const lines = code.split("\n");

  let candidates = [];

  lines.forEach((line, i) => {
    if (line.includes("app.get") || line.includes("app.post")) {
      candidates.push({ line: i + 1, code: line.trim() });
    }
  });

  return candidates;
}

module.exports = { analyze };
