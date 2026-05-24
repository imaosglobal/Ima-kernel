const fs = require("fs");
const path = require("path");
const https = require("https");
const crypto = require("crypto");

const KEY_PATH = process.env.HOME + "/ima_kernel/kernel/cloud/keys.vault.json";

/* ================= KEY ================= */
function key() {
  return JSON.parse(fs.readFileSync(KEY_PATH, "utf8")).primary;
}

/* ================= SMART SCAN ================= */
function scan(dir, maxFiles = 120) {
  const ignore = ["node_modules", ".git"];
  let files = [];

  function walk(d) {
    const items = fs.readdirSync(d, { withFileTypes: true });

    for (const i of items) {
      const full = path.join(d, i.name);

      if (ignore.some(x => full.includes(x))) continue;

      if (i.isDirectory()) walk(full);
      else files.push(full);
    }
  }

  walk(dir);

  // limit כדי לא לקרוס
  files = files.slice(0, maxFiles);

  const out = {};
  for (const f of files) {
    try {
      const content = fs.readFileSync(f, "utf8");
      const rel = path.relative(process.cwd(), f);
      out[rel] = content.slice(0, 4000);
    } catch {}
  }

  return out;
}

/* ================= GEMINI ================= */
function ask(prompt) {
  const payload = JSON.stringify({
    contents: [{
      parts: [{
        text:
`אתה AI בתוך מערכת פיתוח חיה.
אתה עונה בעברית טבעית כמו הממשק הרשמי.

אם יש קוד → החזר PATCH בלבד.
אם לא → הסבר ברור בעברית.

קונטקסט פרויקט:
${prompt}`
      }]
    }]
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: "/v1/models/gemini-3.5-flash:generateContent?key=" + key(),
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, res => {
      let b = "";

      res.on("data", d => b += d);
      res.on("end", () => {
        try {
          const j = JSON.parse(b);
          const text =
            j?.candidates?.[0]?.content?.parts?.map(p => p.text).join("") || "";
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

/* ================= MAIN ================= */
async function main() {
  const input = process.argv.slice(2).join(" ");

  if (!input) {
    console.log("usage: gemini <text>");
    return;
  }

  console.log("[SCAN] project...");
  const project = scan(process.cwd());

  console.log("[ASK] sending to gemini...");

  const res = await ask(`
PROJECT:
${JSON.stringify(project)}

USER:
${input}
`);

  console.log("\n=== GEMINI ===\n");
  console.log(res || "[NO RESPONSE]");
}

main();
