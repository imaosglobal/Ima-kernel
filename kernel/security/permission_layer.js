const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/permissions.json"
)

function boot(){

  if(!fs.existsSync(FILE)){

    fs.writeFileSync(
      FILE,
      JSON.stringify({
        fs:"limited",
        network:"allowed",
        plugins:"sandboxed"
      },null,2)
    )
  }

  console.log("[SECURITY] active")
}

boot()
