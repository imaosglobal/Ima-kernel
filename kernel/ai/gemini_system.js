const fs = require("fs");
const path = require("path");
const https = require("https");
const crypto = require("crypto");

/* ================= CONFIG ================= */
const BASE = process.cwd();
const KEY_PATH = process.env.HOME + "/ima_kernel/kernel/cloud/keys.vault.json";

/* ================= KEY ================= */
function getKey() {
  return JSON.parse(fs.readFileSync(KEY_PATH, "utf8")).primary;
}

/* ================= SAFE SCAN ================= */
function scan(dir, maxFiles = 80) {
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
  files = files.slice(0, maxFiles);

  const out = {};
  for (const f of files) {
    try {
      const rel = path.relative(BASE, f);
      const content = fs.readFileSync(f, "utf8");
      out[rel] = content.slice(0, 3000);
    } catch {}
  }

  return out;
}

/* ================= GEMINI CALL ================= */
function ask(prompt) {
  const payload = JSON.stringify({
    contents: [{
      parts: [{
        text:
`אתה מנוע שיפור קוד.
אם יש שינוי -> החזר PATCH בלבד.
אם לא -> הסבר בעברית.

${prompt}`
      }]
    }]
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: "/v1/models/gemini-3.5-flash:generateContent?key=" + getKey(),
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, res => {
      let b = "";

      res.on("data", d => b += d);
      res.on("end", () => {
        try {
          const j = JSON.parse(b);
          resolve(
            j?.candidates?.[0]?.content?.parts?.map(p => p.text).join("") || ""
          );
        } catch {
          resolve("");
        }
      });
    });

    req.on("error", () => resolve(""));
    req.write(payload);
    req.end();
  });
}

/* ================= APPLY PATCH (SAFE) ================= */
function applyPatch(output) {
  if (!output || !output.includes("diff --git")) {
    console.log("[INFO] no patch to apply");
    return;
  }

  const patchFile = path.join(BASE, "LAST_PATCH.diff");
  fs.writeFileSync(patchFile, output);

  console.log("[PATCH] saved:", patchFile);
}

/* ================= MAIN ENGINE ================= */
async function run(input) {
  console.log("[SCAN] scanning project...");

  const snapshot = scan(BASE);

  console.log("[ASK] Gemini...");

  const res = await ask(`
PROJECT SNAPSHOT:
${JSON.stringify(snapshot)}

TASK:
${input}
`);

  console.log("\n=== GEMINI ===\n");
  console.log(res);

  applyPatch(res);
}

/* ================= WATCH MODE (optional future) ================= */
function watchMode() {
  console.log("[WATCH] not fully enabled yet (next step)");
}

/* ================= EXPORT / CLI ================= */
async function main() {
  const input = process.argv.slice(2).join(" ");

  if (!input) {
    console.log("gemini <instruction>");
    return;
  }

  await run(input);
}

main();
