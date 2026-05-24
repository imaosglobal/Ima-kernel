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
