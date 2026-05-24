const fs = require("fs")
const path = require("path")

const DEVICES = path.join(
  __dirname,
  "../registry/devices.json"
)

function update(){

  const device = {
    id:"termux_local",
    type:"android_termux",
    status:"online",
    ts:Date.now()
  }

  fs.writeFileSync(
    DEVICES,
    JSON.stringify([device],null,2)
  )

  console.log("[MESH] synced")

}

setInterval(update,15000)

update()
