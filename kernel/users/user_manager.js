const fs = require("fs")
const path = require("path")

const FILE = path.join(
  __dirname,
  "../memory/users.json"
)

function ensure(){

  if(!fs.existsSync(FILE)){

    fs.writeFileSync(
      FILE,
      JSON.stringify([
        {
          id:"root",
          role:"creator",
          mode:"full_access"
        }
      ],null,2)
    )
  }
}

function tick(){

  ensure()

  const users = JSON.parse(
    fs.readFileSync(FILE,"utf8")
  )

  console.log(
    "[USERS]",
    users.length
  )
}

setInterval(tick,20000)

tick()
