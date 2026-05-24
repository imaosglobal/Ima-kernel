const fs = require("fs")
const path = require("path")

const FILE =
process.env.HOME +
"/ima_kernel/kernel/cloud/keys.json"

function load(){

try{

if(!fs.existsSync(FILE)){
return null
}

return JSON.parse(
fs.readFileSync(FILE,"utf8")
)

}catch(e){

return null

}

}

function save(primary,secondary){

const data = {
primary: (primary||"").trim(),
secondary: (secondary||"").trim(),
updated: Date.now()
}

fs.mkdirSync(path.dirname(FILE),{recursive:true})

fs.writeFileSync(
FILE,
JSON.stringify(data,null,2)
)

console.log("[KEY VAULT] saved")

return data

}

function get(){

return load()

}

module.exports = {
save,
get
}
