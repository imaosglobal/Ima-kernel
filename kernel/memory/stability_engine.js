const fs = require("fs")
const path = require("path")

const SNAP_DIR = path.join(__dirname, "snapshots")

if(!fs.existsSync(SNAP_DIR)){
  fs.mkdirSync(SNAP_DIR,{recursive:true})
}

function snapshotSystem(){

  const state = {
    ts: Date.now(),
    memory: process.memoryUsage(),
    uptime: process.uptime()
  }

  const file = path.join(
    SNAP_DIR,
    `snapshot_${Date.now()}.json`
  )

  fs.writeFileSync(file, JSON.stringify(state,null,2))

  console.log("[SNAPSHOT]", file)
}

setInterval(snapshotSystem, 20000)

snapshotSystem()
