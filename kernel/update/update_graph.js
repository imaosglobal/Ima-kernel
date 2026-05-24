const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/update_graph.json"
)

function update(){

  const graph = {
    ts:Date.now(),
    nodes:[
      "brain",
      "memory",
      "ui",
      "plugins",
      "runtime"
    ]
  }

  fs.writeFileSync(
    FILE,
    JSON.stringify(graph,null,2)
  )

  console.log("[UPDATE GRAPH] synced")
}

setInterval(update,30000)

update()
