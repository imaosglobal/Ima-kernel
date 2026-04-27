const fs = require("fs");
const { gpt, claude, gemini } = require("./ima_real_llm");

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

// ---------------- CALL ALL ----------------
async function callAll(input) {
  const [g, c, m] = await Promise.all([
    gpt(input),
    claude(input),
    gemini(input)
  ]);

  return { gpt: g, claude: c, gemini: m };
}

// ---------------- CONSENSUS ----------------
function merge(r) {
  return `
IMA CONSENSUS:

GPT:
${r.gpt}

CLAUDE:
${r.claude}

GEMINI:
${r.gemini}

FINAL:
${r.gpt}
`;
}

// ---------------- MAIN ----------------
async function run(input) {
  const mem = loadMemory();

  const responses = await callAll(input);
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

  console.log(final);
}

run(process.argv[2] || "hello");
