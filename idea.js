const { callGemini } = require("./kernel/cloud/gemini_autosync");
const { applyPatch } = require("./kernel/cloud/apply_patch");
const fs = require("fs");

function snapshot() {
  return fs.readFileSync(
    process.env.HOME + "/ima_kernel/kernel/cloud/keys.vault.json",
    "utf8"
  );
}

async function idea(text) {
  console.log("[IDEA]", text);

  const prompt = `
אתה מערכת אוטונומית של קוד.

להלן מצב המערכת:
${snapshot()}

משימה:
${text}

החזר רק PATCHים:

FILE: path
CODE:
...
`;

  const res = await callGemini(prompt);

  console.log("[AI RESPONSE]");
  console.log(res);

  applyPatch(res);

  console.log("[DONE]");
}

module.exports = { idea };
