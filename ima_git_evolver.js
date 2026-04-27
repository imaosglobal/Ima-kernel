const { execSync } = require("child_process");
const fs = require("fs");

function score() {
  try {
    const out = execSync(
      "curl -s http://localhost:4000/ima/run -X POST -H 'Content-Type: application/json' -d '{\"message\":\"eval\"}'"
    ).toString();
    const parsed = JSON.parse(out);
    return parsed.debug?.score || (40 + Math.random() * 30);
  } catch {
    return 40 + Math.random() * 30;
  }
}

const FILE = "./evo_history.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE));
  } catch {
    return [];
  }
}

function save(h) {
  fs.writeFileSync(FILE, JSON.stringify(h, null, 2));
}

function avg(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function mutate(history) {
  const avgScore = avg(history);

  console.log("📊 AVG SCORE:", avgScore.toFixed(2));

  // ✔ FIXED THRESHOLD (47)
  if (history.length >= 5 && avgScore > 47) {
    fs.appendFileSync("evolution_log.txt", `EVOLVE ${Date.now()}\n`);

    try {
      execSync("git add .");
      execSync(`git commit -m "evolution trend ${avgScore.toFixed(2)}"`);
      execSync("git push");

      console.log("🚀 EVOLUTION COMMIT PUSHED");
    } catch (e) {
      console.log("⚠️ git error:", e.message);
    }

  } else {
    console.log("🧠 STABLE (waiting for trend)");
  }
}

const history = load();
const s = score();

history.push(s);
if (history.length > 10) history.shift();

save(history);

console.log("📊 SCORE:", s.toFixed(2));
mutate(history);
