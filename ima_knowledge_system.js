const fs = require("fs");
const { execSync } = require("child_process");

/* ---------- STORAGE ---------- */
const MEMORY = "./memory.json";
const KNOWLEDGE = "./knowledge.json";
const CONFIG = "./ima_config.json";

function load(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function save(p, d){ fs.writeFileSync(p, JSON.stringify(d,null,2)); }

let memory = load(MEMORY, { memory: [] });
let knowledge = load(KNOWLEDGE, { domains: {} });
let config = load(CONFIG, { mode: "stable", evolution: true });

/* ---------- SOURCES (future connectors) ---------- */
function ingestSources(input){
  return {
    raw: input,
    timestamp: Date.now(),
    origin: "local",
  };
}

/* ---------- DOMAIN CLASSIFIER ---------- */
function classify(input){
  if(/כסף|בנק|השקעה/.test(input)) return "finance";
  if(/פסיכולוג|רגש|נפש/.test(input)) return "psychology";
  if(/קוד|תכנות|מערכת/.test(input)) return "technology";
  if(/בריאות|גוף/.test(input)) return "health";
  return "general";
}

/* ---------- LEARN ---------- */
function learn(input){
  const domain = classify(input);
  const data = ingestSources(input);

  if(!knowledge.domains[domain]){
    knowledge.domains[domain] = [];
  }

  knowledge.domains[domain].push(data);

  if(knowledge.domains[domain].length > 200){
    knowledge.domains[domain].shift();
  }

  return domain;
}

/* ---------- REASON ---------- */
function reason(input){
  const domain = classify(input);
  const context = knowledge.domains[domain] || [];

  return `IMA reasoning (${domain}): based on ${context.length} memories → ${input}`;
}

/* ---------- VALIDATION ---------- */
function validate(){
  // בדיקה פשוטה שלא נשבר מבנה
  return knowledge && knowledge.domains;
}

/* ---------- GIT SAFE UPDATE ---------- */
function gitSafe(){
  try {
    if(!validate()) {
      console.log("❌ INVALID KNOWLEDGE - skip commit");
      return;
    }

    execSync("git add .");
    execSync(`git commit -m "IMA knowledge update ${Date.now()}"`);
    execSync("git push origin main");

  } catch(e){
    console.log("⚠ git failed");
  }
}

/* ---------- RUN ---------- */
function run(input){
  console.log("🧠 IMA KNOWLEDGE SYSTEM");

  const domain = learn(input);
  const response = reason(input);

  memory.memory.push({
    input,
    domain,
    time: Date.now()
  });

  save(MEMORY, memory);
  save(KNOWLEDGE, knowledge);

  gitSafe();

  console.log("📚 DOMAIN:", domain);
  console.log("🧠 RESPONSE:", response);
}

/* ---------- EXEC ---------- */
run(process.argv[2] || "test knowledge");
