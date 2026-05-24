const fs = require("fs")
const path = require("path")

const LOCK = path.join(__dirname, "../../runtime.lock")

if(fs.existsSync(LOCK)){
  console.log("[IMA] already running - exit")
  process.exit(1)
}

fs.writeFileSync(LOCK, process.pid.toString())

process.on("exit", ()=>{
  try{ fs.unlinkSync(LOCK) } catch(e){}
})
