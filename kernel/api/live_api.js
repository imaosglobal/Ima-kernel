const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()

app.get("/system",(req,res)=>{

  const memory = JSON.parse(
    fs.readFileSync(
      path.join(__dirname,"../memory/system_state.json"),
      "utf8"
    )
  )

  res.json({
    ok:true,
    memory
  })

})

app.listen(7300,()=>{

  console.log("[LIVE API 2] 7300")

})
