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

// ---------------- LLM MOCKS ----------------
// בעתיד: חיבור אמיתי ל-OpenAI / Claude / Gemini

function gpt(input) {
  return `GPT says: ${input}`;
}

function claude(input) {
  return `Claude says: ${input}`;
}

function gemini(input) {
  return `Gemini says: ${input}`;
}

// ---------------- MULTI CALL ----------------
function callAll(input) {
  return {
    gpt: gpt(input),
    claude: claude(input),
    gemini: gemini(input)
  };
}

// ---------------- CONSENSUS ENGINE ----------------
function merge(responses) {
  // אלגוריתם פשוט: איחוד חכם (בעתיד ניתן לשדרג ל-scoring / embeddings)
  return `
CONSENSUS RESULT:
- ${responses.gpt}
- ${responses.claude}
- ${responses.gemini}

FINAL SYNTHESIS:
${responses.gpt.replace("GPT says:", "").trim()}
`;
}

// ---------------- MAIN ----------------
function run(input) {
  const mem = loadMemory();

  const responses = callAll(input);
  const final = merge(responses);

  const output = {
    input,
    responses,
    final,
    time: Date.now()
  };

  mem.memory.push(output);
  if (mem.memory.length > 100) mem.memory.shift();

  saveMemory(mem);

  console.log("🧠 CONSENSUS OUTPUT:");
  console.log(final);

  return output;
}

run(process.argv[2] || "hello");
