const fs = require("fs")
const path = require("path")

const REGISTRY = path.join(__dirname, "live_registry.json")

function write(data){
  fs.writeFileSync(REGISTRY, JSON.stringify(data,null,2))
}

function update(){
  const snapshot = {
    ts: Date.now(),
    system: "IMA_OS",
    status: "online",
    runtime: process.version,
    memory: process.memoryUsage(),
    uptime: process.uptime()
  }

  write(snapshot)

  console.log("[REGISTRY] updated")
}

setInterval(update,10000)

update()
