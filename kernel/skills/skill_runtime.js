const fs = require("fs")
const path = require("path")

const SKILL_DIR = path.join(__dirname)

function load(){

  const files = fs.readdirSync(SKILL_DIR)

  for(const f of files){

    if(
      f.endsWith(".skill.js")
    ){

      console.log("[SKILL]",f)
    }
  }
}

load()
