const fs = require("fs");
const { ask } = require("./ima_ai_provider");

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

// ---------------- CORE ----------------
async function run(input) {
  const mem = loadMemory();

  const response = await ask(input);

  const output = {
    input,
    response,
    time: Date.now()
  };

  mem.memory.push(output);
  if (mem.memory.length > 200) mem.memory.shift();

  saveMemory(mem);

  console.log("🧠 IMA STABLE OUTPUT:");
  console.log(response);
}

run(process.argv[2] || "hello");
