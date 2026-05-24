const express = require("express")
const path = require("path")

const app = express()

const UI = path.join(
  __dirname,
  "../ui_shell"
)

app.get("/",(req,res)=>{

  res.sendFile(
    path.join(UI,"dashboard.html")
  )

})

app.use(express.static(UI))

app.listen(7200,"0.0.0.0",()=>{

  console.log("[IMA UI] live on 7200")

})
