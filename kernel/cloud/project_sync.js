const { buildSnapshot } = require("./snapshot");
const { callGemini } = require("./gemini_autosync");

async function fullProjectSync(prompt) {
  const snapshot = buildSnapshot();

  const payload = `
אתה ארכיטקט קוד אוטונומי.

להלן כל הפרויקט הנוכחי:
------------------------
${snapshot}

משימתך:
${prompt}

החזר PATCHים בלבד בפורמט:
FILE: path
CODE...
`;

  console.log("[SYNC] sending full project to Gemini...");

  const res = await callGemini(payload);

  console.log("[SYNC RESULT RECEIVED]");
  return res;
}

module.exports = { fullProjectSync };
