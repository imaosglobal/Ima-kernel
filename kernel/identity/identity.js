const fs = require("fs")
const path = require("path")
const crypto = require("crypto")

const FILE = path.join(
  __dirname,
  "../memory/identity.json"
)

function ensureIdentity(){

  if(fs.existsSync(FILE)){

    const data = JSON.parse(
      fs.readFileSync(FILE,"utf8")
    )

    console.log("[IDENTITY] loaded",data.id)

    return data
  }

  const identity = {
    id: crypto.randomUUID(),
    created: Date.now(),
    system: "IMA_OS"
  }

  fs.writeFileSync(
    FILE,
    JSON.stringify(identity,null,2)
  )

  console.log("[IDENTITY] created",identity.id)

  return identity
}

ensureIdentity()
