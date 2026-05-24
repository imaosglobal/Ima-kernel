const https = require("https")
const fs = require("fs")
const path = require("path")

const VAULT = path.join(__dirname, "keys.vault.json")

function loadKeys(){
  try{
    return JSON.parse(fs.readFileSync(VAULT,"utf-8"))
  }catch(e){
    return {}
  }
}

function saveKeys(keys){
  fs.writeFileSync(VAULT, JSON.stringify(keys,null,2))
}

function request(apiKey, prompt){
  return new Promise((resolve)=>{
    const data = JSON.stringify({
      contents: [{ parts: [{ text: prompt }]}]
    })

    const req = https.request({
      hostname: "generativelanguage.googleapis.com",
      path: "/v1beta/models/gemini-1.5-flash:generateContent?key=" + encodeURIComponent(apiKey),
      method: "POST",
      headers: { "Content-Type": "application/json" }
    }, (res)=>{
      let body = ""

      res.on("data", c => body += c)

      res.on("end", ()=>{
        try{
          const json = JSON.parse(body)
          const text =
            json?.candidates?.[0]?.content?.parts?.[0]?.text || ""

          resolve({ ok: true, text })
        }catch(e){
          resolve({ ok: false, text: "" })
        }
      })
    })

    req.on("error", ()=>{
      resolve({ ok: false, text: "" })
    })

    req.write(data)
    req.end()
  })
}

async function validate(keys){
  console.log("[VALIDATE] checking keys")

  if(keys.primary){
    const r = await request(keys.primary, "ping")
    console.log("[PRIMARY]", r.ok ? "CONNECTED" : "FAILED")
  }

  if(keys.secondary){
    const r = await request(keys.secondary, "ping")
    console.log("[SECONDARY]", r.ok ? "CONNECTED" : "FAILED")
  }
}

async function sync(){
  const keys = loadKeys()

  const summary = {
    time: Date.now(),
    keys: Object.keys(keys),
    status: "SYNC"
  }

  const prompt =
`You are IMA sync engine.
Return short status only.
STATE: ${JSON.stringify(summary).slice(0,8000)}`

  if(keys.primary){
    const res = await request(keys.primary, prompt)
    console.log("[PRIMARY RESPONSE]", res.text || "[EMPTY]")
  }

  if(keys.secondary){
    const res = await request(keys.secondary, prompt)
    console.log("[SECONDARY RESPONSE]", res.text || "[EMPTY]")
  }

  console.log("[SYNC COMPLETE]")
}

async function boot(){
  console.log("[IMA CLOUD] boot")

  const keys = loadKeys()

  if(!keys.primary && !keys.secondary){
    console.log("[KEYS] missing - run key setup first")
    return
  }

  await validate(keys)
  await sync()

  setInterval(sync, 60000)
}

boot()

module.exports = { sync, loadKeys, saveKeys }
