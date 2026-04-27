const fs = require("fs");
const { execSync } = require("child_process");

/* ---------- PATHS ---------- */
const CONFIG_PATH = "./ima_config.json";
const MEMORY_PATH = "./memory.json";

/* ---------- IO ---------- */
function loadJSON(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function saveJSON(p, d){ fs.writeFileSync(p, JSON.stringify(d, null, 2)); }

/* ---------- STATE ---------- */
let config = loadJSON(CONFIG_PATH, {
  weights: { relevance: 0.35, clarity: 0.2, usefulness: 0.25, safety: 0.2 },
  version: 1,
  mode: "stable",           // stable | adaptive | creative
  avatar: "default",        // default | calm | explorer | creator
  weights: {                // משקלים לקריטריונים (סכום ~1)
    relevance: 0.35,
    clarity: 0.2,
    usefulness: 0.25,
    safety: 0.2
  },
  evolution: true
});

let memory = loadJSON(MEMORY_PATH, { memory: [] });

/* ---------- PROVIDERS (מועמדים) ---------- */
/* כאן אפשר לחבר בעתיד מודלים/מקורות שונים.
   כרגע – 3 מועמדים פשוטים כדי לאפשר דירוג. */
function providerA(q){ return `תשובה תמציתית: ${q}`; }
function providerB(q){ return `פירוט מעשי עם צעדים: ${q}`; }
function providerC(q){ return `זווית יצירתית/מחקרית: ${q}`; }

/* ---------- SCORING ---------- */
function scoreCandidate(text, query){
  const len = text.length;
  const relevance = Math.min(1, query.length ? (text.includes(query.split(" ")[0]) ? 1 : 0.7) : 0.7);
  const clarity = Math.min(1, 0.4 + (len < 200 ? 0.6 : 0.4));
  const usefulness = Math.min(1, /צעדים|שלב|איך|בפועל/.test(text) ? 1 : 0.7);
  const safety = 1; // כאן ניתן להרחיב בדיקות

  const w = config.weights;
  const total = relevance*w.relevance + clarity*w.clarity + usefulness*w.usefulness + safety*w.safety;

  return { total, breakdown: { relevance, clarity, usefulness, safety } };
}

/* ---------- SELECT ---------- */
function chooseBest(candidates, query){
  const scored = candidates.map(c => {
    const s = scoreCandidate(c.text, query);
    return { ...c, score: s.total, breakdown: s.breakdown };
  });

  scored.sort((a,b)=>b.score-a.score);
  return { best: scored[0], ranked: scored };
}

/* ---------- APPEARANCE (נראות) ---------- */
function updateAppearance(score){
  if (score > 0.8){
    config.mode = "creative";
    config.avatar = "creator";
  } else if (score > 0.6){
    config.mode = "adaptive";
    config.avatar = "explorer";
  } else {
    config.mode = "stable";
    config.avatar = "calm";
  }
}

/* ---------- LEARNING ---------- */
function updateWeights(outcomeScore){
  // עדכון עדין של משקלים לפי הצלחה (0..1)
  const lr = 0.05;
  const w = config.weights;

  // אם הצלחה גבוהה – חזק קריטריונים שתרמו (בקירוב)
  if (outcomeScore > 0.7){
    w.usefulness = Math.min(0.5, w.usefulness + lr);
    w.relevance  = Math.min(0.5, w.relevance  + lr/2);
  } else {
    // אם נמוכה – הגדל בהירות/בטיחות
    w.clarity = Math.min(0.5, w.clarity + lr);
    w.safety  = Math.min(0.5, w.safety  + lr/2);
  }

  // נרמול סכום ל~1
  const sum = w.relevance + w.clarity + w.usefulness + w.safety;
  Object.keys(w).forEach(k => w[k] = w[k]/sum);
}

/* ---------- EVAL OUTCOME (סימולציה בסיסית) ---------- */
function evaluateOutcome(best){
  // כרגע: משתמשים בציון הפנימי כקירוב לתוצאה
  return best.score;
}

/* ---------- GIT ---------- */
function gitSync(){
  try {
    execSync("git add .");
    execSync(`git commit -m "IMA decision update ${Date.now()}"`);
    execSync("git push origin main");
  } catch {}
}

/* ---------- RUN ---------- */
function run(query){
  console.log("🧠 IMA DECISION ENGINE");

  // יצירת מועמדים
  const candidates = [
    { name: "A", text: providerA(query) },
    { name: "B", text: providerB(query) },
    { name: "C", text: providerC(query) }
  ];

  // בחירה
  const { best, ranked } = chooseBest(candidates, query);

  // עדכון נראות/מצב
  updateAppearance(best.score);

  // הערכת תוצאה ולמידה
  const outcome = evaluateOutcome(best);
  if (config.evolution) updateWeights(outcome);

  // שמירה
  const entry = {
    query,
    best: best.text,
    score: best.score,
    ranked: ranked.map(r => ({ name: r.name, score: r.score })),
    mode: config.mode,
    avatar: config.avatar,
    time: Date.now()
  };

  memory.memory.push(entry);
  if (memory.memory.length > 300) memory.memory.shift();

  saveJSON(MEMORY_PATH, memory);
  saveJSON(CONFIG_PATH, config);

  gitSync();

  // פלט
  console.log("🏆 BEST:", best.name, "| SCORE:", best.score.toFixed(2));
  console.log("🎛 MODE:", config.mode, "| AVATAR:", config.avatar);
  console.log("💬", best.text);
}

/* ---------- EXEC ---------- */
run(process.argv[2] || "שאלה לדוגמה");
