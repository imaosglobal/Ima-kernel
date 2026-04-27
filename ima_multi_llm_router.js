const fs = require("fs");

// ---------------- MEMORY ----------------
function loadMemory() {
  try {
    return JSON.parse(fs.readFileSync("./memory.json"));
  } catch {
    return { memory: [] };
  }
}

function saveMemory(mem) {
  fs.writeFileSync("./memory.json", JSON.stringify(mem, null, 2));
}

// ---------------- MOCK LLMs (placeholders) ----------------
// בעתיד כאן נכנסים API אמיתיים

function gptModel(input) {
  return `GPT: ${input}`;
}

function claudeModel(input) {
  return `Claude: ${input}`;
}

function geminiModel(input) {
  return `Gemini: ${input}`;
}

// ---------------- ROUTER ----------------
function route(input) {
  const len = input.length;

  // ניתוב פשוט (ניתן לשדרוג ללוגיקה חכמה / embeddings)
  if (len < 10) return "gpt";
  if (len < 30) return "claude";
  return "gemini";
}

function run(input) {
  const mem = loadMemory();

  const selected = route(input);

  let response;
  if (selected === "gpt") response = gptModel(input);
  if (selected === "claude") response = claudeModel(input);
  if (selected === "gemini") response = geminiModel(input);

  const result = {
    input,
    selected_model: selected,
    response,
    time: Date.now()
  };

  mem.memory.push(result);
  if (mem.memory.length > 100) mem.memory.shift();

  saveMemory(mem);

  console.log("🧠 ROUTER RESULT:");
  console.log(result);

  return result;
}

// ---------------- EXEC ----------------
run(process.argv[2] || "hello");
