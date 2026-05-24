#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel || exit 1

echo "[IMA MASTER] installing unified sync system..."

mkdir -p kernel/cloud
mkdir -p kernel/vibe
mkdir -p kernel/sync
mkdir -p kernel/runtime
mkdir -p logs

########################################
# CLOUD BRIDGE
########################################

cat > kernel/cloud/cloud_bridge.js <<'JS'
const https = require("https")

function sendToCloud(prompt){

  return new Promise((resolve)=>{

    const key = process.env.GEMINI_API_KEY

    if(!key){
      resolve("[ERROR] missing GEMINI_API_KEY")
      return
    }

    const data = JSON.stringify({
      contents:[{
        parts:[{
          text:prompt
        }]
      }]
    })

    const req = https.request({
      hostname:"generativelanguage.googleapis.com",
      path:"/v1beta/models/gemini-1.5-flash:generateContent?key=" + key,
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      }
    },(res)=>{

      let body = ""

      res.on("data",c=>body += c)

      res.on("end",()=>{

        try{

          const json = JSON.parse(body)

          const text =
            json?.candidates?.[0]?.content?.parts?.[0]?.text

          resolve(text || "[EMPTY RESPONSE]")

        } catch(e){

          resolve("[PARSE ERROR] " + e.message)

        }

      })

    })

    req.on("error",(e)=>{
      resolve("[NETWORK ERROR] " + e.message)
    })

    req.write(data)
    req.end()

  })

}

module.exports = { sendToCloud }
JS

########################################
# VIBE ENGINE
########################################

cat > kernel/vibe/vibe_engine.js <<'JS'
const fs = require("fs")
const path = require("path")

const { sendToCloud } =
require("../cloud/cloud_bridge")

async function vibe(input){

  console.log("[VIBE INPUT]",input)

  const cloud = await sendToCloud(`
You are IMA OS autonomous builder.

Return concise engineering response.

Task:
${input}
`)

  console.log("[CLOUD]",cloud)

  if(cloud.includes("plugin")){

    const pluginFile = path.join(
      __dirname,
      "../plugins/cloud_generated.js"
    )

    fs.writeFileSync(
      pluginFile,
`
module.exports = function(){
  console.log("[CLOUD GENERATED PLUGIN]")
}
`
    )

    return {
      type:"plugin",
      file:pluginFile
    }

  }

  return {
    type:"text",
    output:cloud
  }

}

module.exports = { vibe }
JS

########################################
# TERMUX GATEWAY
########################################

cat > kernel/vibe/termux_gateway.js <<'JS'
const { vibe } =
require("./vibe_engine")

async function handle(input){

  const result = await vibe(input)

  console.log("[GATEWAY RESULT]",result)

  return result
}

module.exports = { handle }
JS

########################################
# SYNC ENGINE
########################################

cat > kernel/sync/sync_engine.js <<'JS'
const fs = require("fs")
const path = require("path")

const ROOT =
path.join(__dirname,"../..")

function snapshot(){

  const state = {
    ts:Date.now(),
    files:0
  }

  function walk(dir){

    const files =
      fs.readdirSync(dir)

    for(const f of files){

      const full =
        path.join(dir,f)

      try{

        const stat =
          fs.statSync(full)

        if(stat.isDirectory()){

          if(
            full.includes("node_modules")
          ) continue

          walk(full)

        } else {

          state.files++

        }

      } catch(e){}

    }

  }

  walk(ROOT)

  console.log("[SYNC SNAPSHOT]",state)

  return state
}

setInterval(snapshot,30000)

snapshot()

module.exports = {}
JS

########################################
# REQUIRE GUARD
########################################

cat > kernel/runtime/require_guard.js <<'JS'
const Module = require("module")

const oldRequire =
Module.prototype.require

Module.prototype.require =
function(request){

  try{

    return oldRequire.apply(this,arguments)

  } catch(e){

    console.log(
      "[GUARD]",
      request,
      e.message
    )

    return {}

  }

}
JS

########################################
# AUTO LOADERS
########################################

touch ima.js

grep -q "require_guard" ima.js || \
echo 'require("./kernel/runtime/require_guard")' >> ima.js

grep -q "termux_gateway" ima.js || \
echo 'require("./kernel/vibe/termux_gateway")' >> ima.js

grep -q "sync_engine" ima.js || \
echo 'require("./kernel/sync/sync_engine")' >> ima.js

########################################
# CLEAN OLD LOCKS
########################################

rm -f runtime.lock

########################################
# RESTART
########################################

pkill -f node

sleep 2

nohup node ~/ima_kernel/ima.js \
> ~/ima_kernel/logs/runtime.log 2>&1 &

sleep 3

echo
echo "[IMA MASTER] ONLINE"
echo

tail -20 ~/ima_kernel/logs/runtime.log

