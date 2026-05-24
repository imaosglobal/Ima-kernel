const fs = require("fs")
const path = require("path")
const https = require("https")

const ROOT = process.env.HOME + "/ima_kernel"

function loadKeys(){

const file = ROOT + "/kernel/cloud/keys.json"

if(!fs.existsSync(file)){
console.log("[KEYS] missing")
process.exit(1)
}

return JSON.parse(
fs.readFileSync(file,"utf8")
)

}

function scan(){

const out = []

function walk(dir){

const files = fs.readdirSync(dir)

for(const f of files){

const full = path.join(dir,f)

try{

const stat = fs.statSync(full)

if(stat.isDirectory()){

if(
full.includes("node_modules") ||
full.includes(".git") ||
full.includes("snapshots")
){
continue
}

walk(full)

}
else{

if(
f.endsWith(".js") ||
f.endsWith(".json") ||
f.endsWith(".md")
){

out.push(full)

}

}

}catch(e){}

}

}

walk(ROOT)

return out

}

function summarize(files){

return files.map(f=>{

try{

const txt = fs.readFileSync(f,"utf8")

return {
file:f.replace(ROOT,""),
size:txt.length,
preview:txt.slice(0,500)
}

}catch(e){

return null

}

}).filter(Boolean)

}

function request(apiKey,prompt){

return new Promise((resolve)=>{

const data = JSON.stringify({
contents:[
{
parts:[
{
text:prompt
}
]
}
]
})

const req = https.request({

hostname:"generativelanguage.googleapis.com",

path:
"/v1beta/models/gemini-1.5-flash:generateContent?key=" +
encodeURIComponent(apiKey),

method:"POST",

headers:{
"Content-Type":"application/json"
}

},res=>{

let body=""

res.on("data",d=>body+=d)

res.on("end",()=>{

try{

const json = JSON.parse(body)

const text =
json.candidates?.[0]?.content?.parts?.[0]?.text

resolve(text || "")

}catch(e){

resolve("")

}

})

})

req.on("error",()=>resolve(""))

req.write(data)
req.end()

})

}

function applyPatch(text){

const blocks = text.split("FILE:")

for(const block of blocks){

if(!block.trim()) continue

const lines = block.split("\n")

const file = lines.shift().trim()

const content =
lines.join("\n").replace(/^```js/,"").replace(/^```/,"").replace(/```$/,"")

const target = ROOT + "/" + file

fs.mkdirSync(
path.dirname(target),
{ recursive:true }
)

fs.writeFileSync(target,content)

console.log("[PATCHED]",file)

}

}

async function run(){

console.log("[AUTO BUILDER] start")

const keys = loadKeys()

const files = scan()

console.log("[SCAN]",files.length)

const summary = summarize(files)

const prompt = `
You are autonomous architect for IMA kernel.

Analyze current project state.

Return ONLY valid patches.

Format:

FILE: relative/path/file.js
<full code>

Rules:
- improve architecture
- add missing systems
- repair broken systems
- never explain
- never markdown outside code
- return max 2 files

PROJECT:

${JSON.stringify(summary).slice(0,12000)}
`

const res =
await request(
keys.primary,
prompt
)

if(!res){

console.log("[AI] empty")
return

}

console.log("[AI RESPONSE RECEIVED]")

applyPatch(res)

console.log("[AUTO BUILDER] complete")

}

run()
