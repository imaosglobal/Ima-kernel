const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/discovered_nodes.json"
)

function save(){

  const data = {
    ts:Date.now(),
    nodes:[
      {
        id:"LOCALHOST",
        runtime:"IMA_OS",
        status:"online"
      }
    ]
  }

  fs.writeFileSync(
    FILE,
    JSON.stringify(data,null,2)
  )

  console.log("[DISCOVERY] updated")

}

setInterval(save,30000)

save()
