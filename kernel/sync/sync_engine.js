const fs = require("fs")
const path = require("path")

const ROOT =
path.join(__dirname,"../..")

function snapshot(){

  const state = {
    ts:Date.now(),
    files:0
  }

  function walk(dir){

    const files =
      fs.readdirSync(dir)

    for(const f of files){

      const full =
        path.join(dir,f)

      try{

        const stat =
          fs.statSync(full)

        if(stat.isDirectory()){

          if(
            full.includes("node_modules")
          ) continue

          walk(full)

        } else {

          state.files++

        }

      } catch(e){}

    }

  }

  walk(ROOT)

  console.log("[SYNC SNAPSHOT]",state)

  return state
}

setInterval(snapshot,30000)

snapshot()

module.exports = {}
