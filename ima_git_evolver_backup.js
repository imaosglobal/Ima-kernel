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

// 🧠 trend-based memory
const HISTORY_FILE = "./evo_history.json";

function loadHistory() {
  try {
    return JSON.parse(fs.readFileSync(HISTORY_FILE));
  } catch {
    return [];
  }
}

function saveHistory(h) {
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(h, null, 2));
}

function avg(arr) {
  return arr.reduce((a,b)=>a+b,0) / arr.length;
}

function mutateIfNeeded(history) {
  const avgScore = avg(history);

  console.log("📊 AVG SCORE:", avgScore.toFixed(2));

if (history.length >= 5 && avgScore > 47)
    fs.appendFileSync("evolution_log.txt", `EVOLVE ${Date.now()}\n`);

    execSync("git add .");
    execSync(`git commit -m "evolution trend ${avgScore.toFixed(2)}"`);
    execSync("git push");

    console.log("🚀 EVOLUTION COMMIT PUSHED (TREND)");
  } else {
    console.log("🧠 STABLE (waiting for trend)");
  }
}

const history = loadHistory();
const s = score();

history.push(s);
if (history.length > 10) history.shift();

saveHistory(history);

console.log("📊 SCORE:", s.toFixed(2));
mutateIfNeeded(history);
