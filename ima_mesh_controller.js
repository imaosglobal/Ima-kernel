const fs = require("fs");
const { execSync } = require("child_process");

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

// ---------------- TOOL LAYER ----------------
function gitInfo() {
  try {
    return execSync("git log -1 --oneline").toString().trim();
  } catch {
    return "no git";
  }
}

// ---------------- LLM LAYER (placeholder) ----------------
async function askLLM(input) {
  return {
    model: "ima-local-router",
    response: `processed: ${input}`
  };
}

// ---------------- ORCHESTRATOR ----------------
async function run(input) {
  const mem = loadMemory();

  const llm = await askLLM(input);
  const git = gitInfo();

  const output = {
    input,
    response: llm.response,
    model: llm.model,
    git,
    memory_size: mem.memory.length,
    time: Date.now()
  };

  mem.memory.push(output);
  if (mem.memory.length > 50) mem.memory.shift();

  saveMemory(mem);

  console.log("🧠 IMA OUTPUT:");
  console.log(output);

  return output;
}

// ---------------- EXEC ----------------
run(process.argv[2] || "hello");
