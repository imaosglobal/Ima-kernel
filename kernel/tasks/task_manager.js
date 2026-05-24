const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/tasks.json"
)

function ensure(){

  if(!fs.existsSync(FILE)){

    fs.writeFileSync(
      FILE,
      JSON.stringify([],null,2)
    )
  }
}

function tick(){

  ensure()

  const tasks = JSON.parse(
    fs.readFileSync(FILE,"utf8")
  )

  console.log("[TASKS]",tasks.length)

}

setInterval(tick,15000)

tick()
