const fs = require("fs")
const path = require("path")

const HEALTH_URL = "http://localhost:7000/health"

const state = {
  registry: [],
  brain: { mode: "idle" },
  ui: { mode: "headless" }
}

async function tick(){

  try {
    const res = await fetch(HEALTH_URL)
    const health = await res.json()

    state.brain.mode = health.ok ? "stable" : "recovering"

    // registry simulation (future devices)
    state.registry.push({
      ts: Date.now(),
      status: health.ok ? "online" : "offline"
    })

    // keep last 20 states
    if(state.registry.length > 20){
      state.registry.shift()
    }

    fs.writeFileSync(
      path.join(__dirname, "../memory.json"),
      JSON.stringify(state, null, 2)
    )

    console.log("[IMA CORE LAYER]", state.brain.mode)

  } catch(e){
    console.log("[IMA CORE LAYER ERROR]", e.message)
  }
}

setInterval(tick, 5000)
