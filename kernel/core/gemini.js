const fs = require("fs");
const https = require("https");
const path = require("path");

const BASE = process.cwd();

function scan(dir, out = {}) {
  const ignore = ["node_modules", ".git"];
  for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, f.name);
    if (ignore.some(i => full.includes(i))) continue;

    if (f.isDirectory()) scan(full, out);
    else {
      try {
        out[path.relative(BASE, full)] = fs.readFileSync(full, "utf8").slice(0, 8000);
      } catch {}
    }
  }
  return out;
}

function ask(prompt) {
  const key = process.env.GEMINI_KEY || "";
  const data = JSON.stringify({
    contents: [{ parts: [{ text: prompt }]}]
  });

  return new Promise(resolve => {
    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: "/v1/models/gemini-2.5-flash:generateContent?key=" + key,
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, res => {
      let b = "";
      res.on("data", d => b += d);
      res.on("end", () => {
        try {
          const j = JSON.parse(b);
          resolve(j?.candidates?.[0]?.content?.parts?.map(p=>p.text).join("") || "");
        } catch {
          resolve("");
        }
      });
    });

    req.on("error", () => resolve(""));
    req.write(data);
    req.end();
  });
}

async function run(input) {
  const project = scan(process.cwd());

  const prompt =
`אתה מנוע שיפור מערכת.
יש לך snapshot מלא של הפרויקט.

PROJECT:
${JSON.stringify(project)}

USER:
${input}

החזר PATCH בלבד או תשובה בעברית.`;

  console.log("[SCAN] done");
  console.log("[ASK] Gemini...");
  const res = await ask(prompt);

  console.log("\\n=== GEMINI ===\\n");
  console.log(res || "[NO RESPONSE]");
}

run(process.argv.slice(2).join(" "));
