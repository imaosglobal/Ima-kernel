const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/decisions.json"
)

function decide(){

  const decision = {
    ts:Date.now(),
    action:"maintain_stability",
    confidence:0.93
  }

  fs.writeFileSync(
    FILE,
    JSON.stringify(decision,null,2)
  )

  console.log(
    "[DECISION]",
    decision.action
  )
}

setInterval(decide,20000)

decide()
