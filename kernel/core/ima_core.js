const https = require("https");
const fs = require("fs");
const path = require("path");

/* ================= KEYS ================= */

function loadKeys() {
  return JSON.parse(
    fs.readFileSync(
      path.join(process.env.HOME, "ima_kernel/kernel/cloud/keys.vault.json"),
      "utf8"
    )
  );
}

/* ================= MODEL SYNC ================= */

async function fetchModels(key) {
  return new Promise((resolve) => {
    https.get(
      "https://generativelanguage.googleapis.com/v1/models?key=" + key,
      (res) => {
        let b = "";
        res.on("data", (d) => (b += d));
        res.on("end", () => {
          try {
            const j = JSON.parse(b);
            const models = (j.models || []).map((m) =>
              m.name.replace("models/", "")
            );
            resolve(models);
          } catch {
            resolve([]);
          }
        });
      }
    );
  });
}

let CACHE = [];

async function syncModels() {
  const keys = loadKeys();
  const models = await fetchModels(keys.primary);

  if (models.length) {
    CACHE = models;
    console.log("[MODEL SYNC] updated:", models.length);
  } else {
    console.log("[MODEL SYNC] fallback cache");
  }

  return CACHE;
}

/* ================= MODEL PICK ================= */

function pickModel(models) {
  const priority = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash"
  ];

  for (const p of priority) {
    const found = models.find((m) => m.includes(p));
    if (found) return found;
  }

  return models[0];
}

/* ================= GEMINI CALL ================= */

async function callGemini(prompt) {
  const keys = loadKeys();
  const models = CACHE.length ? CACHE : await syncModels();

  const model = pickModel(models);

  console.log("[MODEL ACTIVE]", model);

  const data = JSON.stringify({
    contents: [{ parts: [{ text: "ענה בעברית בצורה ברורה:\n" + prompt }] }]
  });

  return new Promise((resolve) => {
    const req = https.request(
      {
        hostname: "generativelanguage.googleapis.com",
        path: `/v1/models/${model}:generateContent?key=` + keys.primary,
        method: "POST",
        headers: { "Content-Type": "application/json" }
      },
      (res) => {
        let b = "";
        res.on("data", (d) => (b += d));
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
      }
    );

    req.on("error", () => resolve(null));
    req.write(data);
    req.end();
  });
}

/* ================= IDEA ENGINE ================= */

async function idea(text) {
  console.log("[IDEA]", text);

  const prompt = `
אתה ארכיטקט מערכת.

קח את הרעיון הבא ושפר את כל הפרויקט.

חוקים:
- החזר רק PATCH
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

/* ================= AUTO SYNC ================= */

async function startAutoSync(interval = 60000) {
  await syncModels();
  setInterval(syncModels, interval);
  console.log("[AUTO SYNC] running");
}

/* ================= EXPORT ================= */

module.exports = {
  callGemini,
  syncModels,
  startAutoSync,
  idea
};
