const fs = require("fs")
const path = require("path")

const QUEUE = path.join(
  __dirname,
  "../registry/patch_queue.json"
)

function ensure(){

  if(!fs.existsSync(QUEUE)){

    fs.writeFileSync(
      QUEUE,
      JSON.stringify([],null,2)
    )

  }

}

ensure()

console.log("[PATCH QUEUE] ready")
