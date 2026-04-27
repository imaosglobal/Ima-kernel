const fs = require("fs");
const crypto = require("crypto");
const { execSync } = require("child_process");

/* ---------------- CONFIG ---------------- */
const CONFIG_PATH = "./ima_config.json";
const MEMORY_PATH = "./ima_private_memory.enc";
const PUBLIC_LOG = "./ima_public_log.json";

const SECRET_KEY = crypto.createHash("sha256").update(
  process.env.IMA_KEY || "default_dev_key_change_me"
).digest();

/* IV קבוע (למערכת שלך זה מספיק כרגע, בעתיד אפשר רנדומלי) */
const IV = Buffer.alloc(16, 0);

/* ---------------- UTILS ---------------- */
function loadJSON(p, fb){ try { return JSON.parse(fs.readFileSync(p)); } catch { return fb; } }
function saveJSON(p, d){ fs.writeFileSync(p, JSON.stringify(d, null, 2)); }

/* ---------------- ENCRYPTION (FIXED) ---------------- */
function encrypt(data){
  const cipher = crypto.createCipheriv("aes-256-ctr", SECRET_KEY, IV);
  return Buffer.concat([
    cipher.update(JSON.stringify(data)),
    cipher.final()
  ]).toString("hex");
}

function decrypt(data){
  try {
    const decipher = crypto.createDecipheriv("aes-256-ctr", SECRET_KEY, IV);
    const decrypted = Buffer.concat([
      decipher.update(Buffer.from(data, "hex")),
      decipher.final()
    ]);
    return JSON.parse(decrypted.toString());
  } catch {
    return { memory: [] };
  }
}

/* ---------------- STATE ---------------- */
let config = loadJSON(CONFIG_PATH, {
  mode: "stable",
  evolution: true
});

let privateMemory = loadJSON(MEMORY_PATH, { memory: [] });

/* ---------------- CORE ---------------- */
function think(input){
  return `IMA CORE RESPONSE: ${input}`;
}

/* ---------------- LEARNING ---------------- */
function learn(input, output){
  privateMemory.memory.push({
    input,
    output,
    time: Date.now()
  });

  if(privateMemory.memory.length > 500){
    privateMemory.memory.shift();
  }
}

/* ---------------- EVOLUTION ---------------- */
function evolve(){
  const size = privateMemory.memory.length;
  if(size > 300) config.mode = "adaptive";
  if(size > 450) config.mode = "creative";
}

/* ---------------- SAVE ---------------- */
function saveAll(){
  saveJSON(CONFIG_PATH, config);

  const encrypted = encrypt(privateMemory);
  fs.writeFileSync(MEMORY_PATH, encrypted);

  saveJSON(PUBLIC_LOG, {
    size: privateMemory.memory.length,
    mode: config.mode,
    time: Date.now()
  });
}

/* ---------------- GIT ---------------- */
function gitSync(){
  try {
    execSync("git add .");
    execSync(`git commit -m "IMA secure update ${Date.now()}"`);
    execSync("git push origin main");
  } catch {}
}

/* ---------------- RUN ---------------- */
function run(input){
  console.log("🧠 IMA FULL SECURE SYSTEM");

  const output = think(input);

  learn(input, output);
  evolve();
  saveAll();
  gitSync();

  console.log("📊 MODE:", config.mode);
  console.log("💬", output);
}

run(process.argv[2] || "hello");
