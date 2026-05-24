const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/shell_state.json"
)

function render(){

  const shell = {
    ts:Date.now(),
    mode:"adaptive",
    ui:"aurora"
  }

  fs.writeFileSync(
    FILE,
    JSON.stringify(shell,null,2)
  )

  console.log("[SHELL] adaptive")
}

setInterval(render,25000)

render()
