const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()

function read(file){
  try{
    return JSON.parse(fs.readFileSync(file,"utf8"))
  }catch(e){
    return {}
  }
}

app.get("/live",(req,res)=>{

  const registry = read(
    path.join(__dirname,"../registry/live_registry.json")
  )

  const memory = read(
    path.join(__dirname,"../../memory.json")
  )

  res.json({
    ok:true,
    registry,
    memory,
    ts:Date.now()
  })

})

app.listen(7100,()=>{

  console.log("[LIVE API] 7100")

})
