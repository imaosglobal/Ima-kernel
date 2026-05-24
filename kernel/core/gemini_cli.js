const fs = require("fs");
const path = require("path");
const https = require("https");
const crypto = require("crypto");

/* ================= CONFIG ================= */
const BASE = process.cwd();
const KEY_PATH = process.env.HOME + "/ima_kernel/kernel/cloud/keys.vault.json";

/* ================= LOAD KEY ================= */
function getKey() {
  return JSON.parse(fs.readFileSync(KEY_PATH, "utf8")).primary;
}

/* ================= SCAN PROJECT ================= */
function scanDir(dir, base = dir, out = {}) {
  const ignore = ["node_modules", ".git", "logs"];
  const items = fs.readdirSync(dir, { withFileTypes: true });

  for (const item of items) {
    const full = path.join(dir, item.name);
    const rel = path.relative(base, full);

    if (ignore.some(x => rel.includes(x))) continue;

    if (item.isDirectory()) {
      scanDir(full, base, out);
    } else {
      try {
        const content = fs.readFileSync(full, "utf8");
        const hash = crypto.createHash("sha256").update(content).digest("hex");

        out[rel] = {
          hash,
          content: content.slice(0, 8000) // limit safety
        };
      } catch {}
    }
  }

  return out;
}

/* ================= CALL GEMINI ================= */
function callGemini(prompt) {
  const key = getKey();

  const payload = JSON.stringify({
    contents: [{
      parts: [{
        text:
`אתה מנוע שיפור קוד ברמת מערכת.
אתה מקבל snapshot של פרויקט שלם.

חוקים:
- החזר PATCH בלבד או תשובה בעברית אם לא קוד
- אל תמציא קבצים שלא קיימים
- אל תשבור קוד קיים
- תהיה מדויק

PROMPT:
${prompt}`
      }]
    }]
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
          const text =
            j?.candidates?.[0]?.content?.parts?.map(p => p.text).join("") || null;
          resolve(text);
        } catch {
          resolve(null);
        }
      });
    });

    req.on("error", () => resolve(null));
    req.write(payload);
    req.end();
  });
}

/* ================= IDEA ENGINE ================= */
async function idea(text) {
  console.log("[IDEA]", text);

  const snapshot = scanDir(BASE);

  const prompt = `
אני שולח לך פרויקט שלם כסנאפשוט JSON.
תנתח הכל ותשפר אותו.

פרויקט:
${JSON.stringify(snapshot, null, 2)}

בקשה:
${text}
`;

  const res = await callGemini(prompt);

  if (!res) {
    console.log("[AI] no response");
    return;
  }

  console.log("\n=== GEMINI RESPONSE ===\n");
  console.log(res);
}

/* ================= CLI ================= */
async function main() {
  const input = process.argv.slice(2).join(" ");
  if (!input) {
    console.log("Usage: node gemini_cli.js <instruction in Hebrew>");
    return;
  }

  await idea(input);
}

main();

module.exports = { idea };
