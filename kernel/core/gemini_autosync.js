const https = require("https");
const fs = require("fs");

function loadKey() {
  return JSON.parse(
    fs.readFileSync(process.env.HOME + "/ima_kernel/kernel/cloud/keys.vault.json", "utf8")
  ).primary;
}

async function syncModels() {
  const key = loadKey();

  return new Promise((resolve) => {
    https.get(
      "https://generativelanguage.googleapis.com/v1/models?key=" + key,
      (res) => {
        let b = "";
        res.on("data", d => b += d);
        res.on("end", () => {
          try {
            const j = JSON.parse(b);
            const models = (j.models || []).map(m => m.name.replace("models/", ""));
            console.log("[MODEL SYNC]", models.length);
            resolve(models);
          } catch {
            resolve([]);
          }
        });
      }
    );
  });
}

function pickModel(models) {
  const priority = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash"
  ];

  for (const p of priority) {
    const found = models.find(m => m.includes(p));
    if (found) return found;
  }

  return models[0] || "gemini-2.5-flash";
}

async function callGemini(prompt) {
  const key = loadKey();
  const models = await syncModels();
  const model = pickModel(models);

  console.log("[MODEL]", model);

  const data = JSON.stringify({
    contents: [{ parts: [{ text: prompt }] }]
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: `/v1/models/${model}:generateContent?key=` + key,
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, res => {
      let b = "";
      res.on("data", d => b += d);
      res.on("end", () => {
        try {
          const j = JSON.parse(b);
          resolve(j.candidates?.[0]?.content?.parts?.[0]?.text || null);
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

module.exports = { callGemini, syncModels };
