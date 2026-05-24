const https = require("https");
const fs = require("fs");
const { pickModel } = require("./model_router");

function loadKey(){
  return JSON.parse(
    fs.readFileSync(process.env.HOME+'/ima_kernel/kernel/cloud/keys.vault.json','utf8')
  ).primary;
}

async function callGemini(prompt){

  const key = loadKey();
  const model = await pickModel();

  console.log("[MODEL SELECTED]", model);

  const data = JSON.stringify({
    contents: [{ parts: [{ text: prompt }]}]
  });

  return new Promise((resolve)=>{
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
          resolve(
            j.candidates?.[0]?.content?.parts?.[0]?.text || null
          );
        } catch(e){
          resolve(null);
        }
      });

    });

    req.on("error", err => {
      console.log("[ERROR]", err.message);
      resolve(null);
    });

    req.write(data);
    req.end();
  });
}

module.exports = { callGemini };
