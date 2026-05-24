const fs = require("fs")
const path = require("path")

const FREEZE_FILE = path.join(__dirname, "../../memory/freeze_state.json")

let frozen = false
let freezeCounter = 0

function setFreeze(state){
  frozen = state

  fs.writeFileSync(
    FREEZE_FILE,
    JSON.stringify({
      frozen,
      ts: Date.now()
    }, null, 2)
  )

  console.log("[FREEZE]", frozen ? "ON" : "OFF")
}

function checkFreeze(stabilityState){

  if(stabilityState === "TRUE_STABLE"){
    freezeCounter++
  } else {
    freezeCounter = 0
  }

  if(freezeCounter >= 3 && !frozen){
    setFreeze(true)
  }

  if(stabilityState !== "TRUE_STABLE" && frozen){
    setFreeze(false)
  }

  return frozen
}

module.exports = { checkFreeze }
