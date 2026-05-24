#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo "[IMA] bootstrap start"

mkdir -p "$ROOT/kernel/cloud"
mkdir -p "$ROOT/kernel/projects"
mkdir -p "$ROOT/kernel/state"
mkdir -p "$ROOT/logs"

if [ ! -f "$ROOT/kernel/cloud/api_keys.json" ]; then

echo ""
echo "PRIMARY GEMINI API KEY:"
read PRIMARY

echo ""
echo "SECONDARY GEMINI API KEY:"
read SECONDARY

cat > "$ROOT/kernel/cloud/api_keys.json" <<KEYS
{
"primary":"$PRIMARY",
"secondary":"$SECONDARY"
}
KEYS

echo "[KEYS] saved"

fi

cat > "$ROOT/kernel/cloud/cloud_sync.js" <<'NODE'
const fs = require("fs")
const path = require("path")
const https = require("https")

const ROOT = path.join(__dirname,"../../")

const KEYS_FILE =
path.join(__dirname,"api_keys.json")

const PROJECTS_DIR =
path.join(ROOT,"kernel/projects")

const STATE_DIR =
path.join(ROOT,"kernel/state")

const STATE_FILE =
path.join(STATE_DIR,"sync_state.json")

function loadKeys(){

try{
return JSON.parse(
fs.readFileSync(KEYS_FILE,"utf8")
)
}catch(e){
return {}
}

}

function scan(dir,arr=[]){

if(!fs.existsSync(dir)) return arr

const files = fs.readdirSync(dir)

for(const file of files){

const full = path.join(dir,file)

try{

  const stat = fs.statSync(full)

  if(stat.isDirectory()){

    scan(full,arr)

  } else {

    arr.push({
      path: full,
      size: stat.size
    })

  }

}catch(e){}

}

return arr

}

function request(apiKey,prompt){

return new Promise((resolve)=>{

const body = JSON.stringify({
  contents:[
    {
      parts:[
        {
          text:prompt
        }
      ]
    }
  ]
})

const req = https.request({

  hostname:
  "generativelanguage.googleapis.com",

  path:
  "/v1beta/models/gemini-1.5-flash:generateContent?key="
  + apiKey,

  method:"POST",

  headers:{
    "Content-Type":"application/json"
  }

},(res)=>{

  let data=""

  res.on("data",(c)=>{
    data += c
  })

  res.on("end",()=>{

    try{

      const json = JSON.parse(data)

      const text =
      json?.candidates?.[0]?.content?.parts?.[0]?.text

      resolve({
        ok:true,
        text:text || "[EMPTY RESPONSE]"
      })

    }catch(e){

      resolve({
        ok:false,
        text:"[PARSE ERROR]"
      })

    }

  })

})

req.on("error",()=>{

  resolve({
    ok:false,
    text:"[REQUEST ERROR]"
  })

})

req.write(body)
req.end()

})

}

async function validateKeys(){

const keys = loadKeys()

console.log("[VALIDATE] checking keys")

let primaryOk = false
let secondaryOk = false

if(keys.primary){

const res =
await request(
  keys.primary,
  "PING PRIMARY"
)

primaryOk = res.ok

console.log(
  "[PRIMARY]",
  res.ok ? "CONNECTED" : "FAILED"
)

}

if(keys.secondary){

const res =
await request(
  keys.secondary,
  "PING SECONDARY"
)

secondaryOk = res.ok

console.log(
  "[SECONDARY]",
  res.ok ? "CONNECTED" : "FAILED"
)

}

return primaryOk || secondaryOk

}

async function sync(){

const keys = loadKeys()

const files = scan(PROJECTS_DIR)

const snapshot = {

time:new Date().toISOString(),

total_files:files.length,

files:files.slice(0,300)

}

fs.writeFileSync(
STATE_FILE,
JSON.stringify(snapshot,null,2)
)

console.log(
"[SYNC] files:",
files.length
)

const payload =
"IMA FULL PROJECT SYNC\n\n"

+ JSON.stringify(snapshot).slice(0,20000)

if(keys.primary){

const res =
await request(
  keys.primary,
  payload
)

console.log(
  "[PRIMARY RESPONSE]",
  res.text.slice(0,200)
)

}

if(keys.secondary){

const res =
await request(
  keys.secondary,
  payload
)

console.log(
  "[SECONDARY RESPONSE]",
  res.text.slice(0,200)
)

}

console.log("[SYNC COMPLETE]")

}

async function boot(){

console.log("[IMA CLOUD] boot")

const ok = await validateKeys()

if(!ok){

console.log(
  "[IMA CLOUD] no valid keys"
)

process.exit(1)

}

console.log(
"[IMA CLOUD] keys verified"
)

await sync()

setInterval(sync,60000)

}

boot()
NODE

chmod +x "$ROOT/kernel/cloud/cloud_sync.js"

if [ ! -d "$ROOT/kernel/projects/ima_core" ]; then

cp -r "$ROOT" "$ROOT/kernel/projects/ima_core"

fi

grep -q "cloud_sync" "$ROOT/ima.js" || echo '
require("./kernel/cloud/cloud_sync")
' >> "$ROOT/ima.js"

pkill -f node >/dev/null 2>&1

nohup node "$ROOT/ima.js" > "$ROOT/logs/runtime.log" 2>&1 &

sleep 5

echo ""
echo "[IMA] runtime status:"
tail -20 "$ROOT/logs/runtime.log"

echo ""
echo "[IMA] sync layer active"

