const fs = require("fs");
const path = require("path");
const https = require("https");

const ROOT = process.env.HOME + "/ima_kernel";

/* ================= FILE WRITE SAFE ================= */
function writeFile(filePath, content) {
  const full = path.join(ROOT, filePath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, "utf8");
  console.log("[WRITE]", filePath);
}

/* ================= LOAD KEYS ================= */
function loadKeys() {
  return JSON.parse(
    fs.readFileSync(ROOT + "/kernel/cloud/keys.vault.json", "utf8")
  );
}

/* ================= GEMINI CALL ================= */
function callGemini(prompt) {
  const key = loadKeys().primary;

  const data = JSON.stringify({
    contents: [{ parts: [{ text: "ענה בעברית קצרה וברורה:\n" + prompt }] }]
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: "/v1/models/gemini-3.5-flash:generateContent?key=" + key,
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, res => {
      let b = "";

      res.on("data", d => b += d);

      res.on("end", () => {
        try {
          const j = JSON.parse(b);
          resolve(
            j.candidates?.[0]?.content?.parts?.[0]?.text || null
          );
        } catch {
          resolve(null);
        }
      });
    });

    req.on("error", () => resolve(null));
    req.write(data);
    req.end();
  });
}

/* ================= IDEA ENGINE ================= */
async function idea(text) {
  console.log("[IDEA]", text);

  const prompt = `
אתה ארכיטקט מערכת IMA.

חוקים:
- רק Node.js
- רק קבצים בתוך הפרויקט
- החזר PATCH בלבד (git diff)
- עד 2 קבצים
- בלי הסברים

רעיון:
${text}
`;

  const res = await callGemini(prompt);

  if (!res) {
    console.log("[AI] empty");
    return null;
  }

  console.log("[AI PATCH RECEIVED]");
  return res;
}

/* ================= APPLY PATCH SIMPLE ================= */
function applyPatch(text) {
  console.log("[APPLY] (stub)");
  console.log(text);
}

/* ================= ENTRY ================= */
module.exports = {
  idea,
  callGemini,
  writeFile,
  applyPatch
};
