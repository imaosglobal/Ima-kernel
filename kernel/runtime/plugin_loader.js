const fs = require("fs")
const path = require("path")

const PLUGIN_DIR = path.join(__dirname, "../plugins")

function loadPlugins(){
  if(!fs.existsSync(PLUGIN_DIR)) return

  const files = fs.readdirSync(PLUGIN_DIR)

  for(const f of files){
    if(f.endsWith(".js")){
      try {
        require(path.join(PLUGIN_DIR, f))
        console.log("[PLUGIN LOADED]", f)
      } catch(e){
        console.log("[PLUGIN ERROR]", f)
      }
    }
  }
}

module.exports = { loadPlugins }
