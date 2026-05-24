const fs = require("fs")
const path = require("path")

const MEMORY = path.join(
  __dirname,
  "../memory/brain_state.json"
)

function think(){

  const state = {
    ts:Date.now(),
    mode:"learning",
    decisions:[
      "optimize_runtime",
      "reduce_failures",
      "improve_ui"
    ]
  }

  fs.writeFileSync(
    MEMORY,
    JSON.stringify(state,null,2)
  )

  console.log("[LOCAL BRAIN] thinking")

}

setInterval(think,25000)

think()
