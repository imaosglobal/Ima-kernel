const fs = require("fs")
const path = require("path")

const MEMORY_PATH = path.join(__dirname, "../../memory.json")

async function run(){

  try {

    const res = await fetch("http://localhost:7000/health")
    const json = await res.json()

    const memory = {
      ts: Date.now(),
      health: json,
      status: json.ok ? "stable" : "unstable"
    }

    fs.writeFileSync(
      MEMORY_PATH,
      JSON.stringify(memory, null, 2)
    )

    console.log("[MEMORY WRITTEN]", memory.status)

  } catch(e){
    console.log("[MEMORY ERROR]", e.message)
  }
}

setInterval(run, 10000)
