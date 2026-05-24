const fs = require("fs")
const path = require("path")
const crypto = require("crypto")

const ROOT = path.join(__dirname, "../..")

const SCOPE = [
  "ima.js",
  "server.js",
  "kernel/brain",
  "kernel/memory",
  "kernel/os",
  "kernel/plugins"
]

let lastHash = null
let stableCount = 0

function scan(){
  let files = []

  for(const item of SCOPE){
    const full = path.join(ROOT,item)

    try{
      const stat = fs.statSync(full)

      if(stat.isDirectory()){
        const inner = fs.readdirSync(full)
        for(const f of inner){
          files.push(path.join(full,f))
        }
      } else {
        files.push(full)
      }
    } catch(e){}
  }

  return files
}

function hash(files){
  const h = crypto.createHash("sha256")

  for(const f of files){
    try{
      const c = fs.readFileSync(f,"utf8")
      h.update(f)
      h.update(c)
    } catch(e){}
  }

  return h.digest("hex")
}

function evaluate(currentHash){

  if(lastHash === currentHash){
    stableCount++
  } else {
    stableCount = 0
  }

  lastHash = currentHash

  if(stableCount >= 3){
    return "TRUE_STABLE"
  }

  return "OPTIMIZING"
}

function tick(){

  const files = scan()
  const h = hash(files)
  const state = evaluate(h)

  console.log("[STABILITY CORE]", state, "| files:", files.length)
}

setInterval(tick,15000)
tick()

module.exports = {}
