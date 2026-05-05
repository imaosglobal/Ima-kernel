const fs = require("fs");
const { execSync } = require("child_process");

function read(path, fallback) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf-8"));
  } catch {
    return fallback;
  }
}

function runSandbox(file) {
  try {
    const output = execSync(`node ${file}`, {
      timeout: 3000,
      encoding: "utf-8"
    });
    return { ok: true, output };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

function safetyCheck() {
  const state = read("ima_state.json", {});
  const files = state.generated_outputs || [];

  const results = [];

  for (const f of files) {
    const fullPath = f.replace("~", process.env.HOME);

    const res = runSandbox(fullPath);

    results.push({
      file: f,
      ok: res.ok
    });

    console.log("[SANDBOX]", f, res.ok ? "OK" : "FAIL");
  }

  state.safety_results = results;
  fs.writeFileSync("ima_state.json", JSON.stringify(state, null, 2));

  return results;
}

module.exports = { safetyCheck };
