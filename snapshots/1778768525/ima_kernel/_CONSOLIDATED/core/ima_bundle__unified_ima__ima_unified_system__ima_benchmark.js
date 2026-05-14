const { execSync } = require("child_process");

function hit() {
  const start = Date.now();
  try {
    execSync("curl -s http://localhost:3000");
  } catch {}
  return Date.now() - start;
}

function runTest() {
  let total = 0;
  let runs = 5;

  for (let i = 0; i < runs; i++) {
    total += hit();
  }

  const avg = total / runs;
  console.log("📊 AVG RESPONSE:", avg);
  return avg;
}

module.exports = { runTest };
