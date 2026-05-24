const https = require("https");
const fs = require("fs");

function loadKey(){
  return JSON.parse(
    fs.readFileSync(process.env.HOME+'/ima_kernel/kernel/cloud/keys.vault.json','utf8')
  );
}

function getModels(key){
  return new Promise((resolve)=>{
    https.get(
      'https://generativelanguage.googleapis.com/v1/models?key='+key,
      res=>{
        let b='';
        res.on('data',d=>b+=d);
        res.on('end',()=>{
          try{
            const j=JSON.parse(b);
            resolve((j.models||[]).map(m=>m.name));
          }catch(e){
            resolve([]);
          }
        });
      }
    );
  });
}

async function pickModel(){
  const keys = loadKey();
  const models = await getModels(keys.primary);

  const priority = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash"
  ];

  for(const p of priority){
    const found = models.find(m => m.includes(p));
    if(found) return found.replace("models/","");
  }

  return models[0]?.replace("models/","") || null;
}

module.exports = { pickModel };
