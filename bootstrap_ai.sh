#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo "[BOOTSTRAP] starting full AI system setup..."

mkdir -p "$ROOT/kernel/core"
mkdir -p "$ROOT/kernel/cloud"

# ================= GEMINI CORE =================
cat > "$ROOT/kernel/cloud/gemini_autosync.js" <<'JS'
const fs = require("fs");
const https = require("https");

function loadKeys(){
  return JSON.parse(fs.readFileSync(process.env.HOME+"/ima_kernel/kernel/cloud/keys.vault.json","utf8"));
}

function callGemini(prompt){
  const key = loadKeys().primary;

  const data = JSON.stringify({
    contents:[{parts:[{text: prompt}]}]
  });

  return new Promise((resolve)=>{
    const req = https.request({
      hostname:"generativelanguage.googleapis.com",
      path:"/v1/models/gemini-3.5-flash:generateContent?key="+key,
      method:"POST",
      headers:{"Content-Type":"application/json"}
    },res=>{
      let b="";
      res.on("data",d=>b+=d);
      res.on("end",()=>{
        try{
          const j=JSON.parse(b);
          resolve(j.candidates?.[0]?.content?.parts?.[0]?.text || null);
        }catch{
          resolve(null);
        }
      });
    });

    req.on("error",()=>resolve(null));
    req.write(data);
    req.end();
  });
}

module.exports = { callGemini };
JS

# ================= IDEA ENGINE =================
cat > "$ROOT/kernel/core/idea_engine.js" <<'JS'
const fs = require("fs");
const path = require("path");
const { callGemini } = require("../cloud/gemini_autosync");

function loadProject(){
  const root = path.join(process.env.HOME,"ima_kernel");
  return fs.readdirSync(root);
}

function apply(res){
  console.log("[PATCH RAW]");
  console.log(res);
}

async function idea(text){
  console.log("[IDEA]",text);

  const project = loadProject();

  const prompt = `
אתה ארכיטקט מערכת Node.js.

פרויקט:
${JSON.stringify(project)}

חוקים:
- רק Node.js
- רק PATCHים
- עד 2 קבצים
- בלי הסברים

רעיון:
${text}
`;

  const res = await callGemini(prompt);

  if(!res){
    console.log("[AI EMPTY]");
    return;
  }

  console.log("[AI PATCH RECEIVED]");
  apply(res);
}

module.exports = { idea };
JS

# ================= BOOT TEST =================
node -e "console.log('[BOOTSTRAP OK]')"

echo "[BOOTSTRAP COMPLETE]"
