const fs = require("fs");

function read(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf-8"));
  } catch {
    return fallback;
  }
}

function writeFile(path, content) {
  fs.writeFileSync(path, content);
}

function generateCodeFromPlan() {
  const state = read("ima_state.json", {});
  const plan = state.execution_plan || [];

  const outputs = [];

  for (const p of plan) {
    if (p.action === "create_module") {
      const code = `
// AUTO GENERATED MODULE
module.exports = function ${p.target}() {
  console.log("Running auto module: ${p.description}");
};
`;
      const file = `~/ima_core/kernel/generated_${p.target}.js`;
      writeFile(file, code);
      outputs.push(file);
    }

    if (p.action === "update_routes") {
      const code = `
// AUTO ROUTE PATCH
console.log("API extension loaded: ${p.description}");
`;
      const file = `~/ima_core/kernel/generated_routes_patch.js`;
      writeFile(file, code);
      outputs.push(file);
    }

    if (p.action === "update_cli") {
      const code = `
// AUTO CLI PATCH
console.log("CLI extension loaded: ${p.description}");
`;
      const file = `~/ima_core/kernel/generated_cli_patch.js`;
      writeFile(file, code);
      outputs.push(file);
    }
  }

  state.generated_outputs = outputs;
  fs.writeFileSync("ima_state.json", JSON.stringify(state, null, 2));

  return outputs;
}

module.exports = { generateCodeFromPlan };
