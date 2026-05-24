const https = require("https")

function request(key, prompt){

return new Promise((resolve)=>{

const data = JSON.stringify({
contents: [{
parts: [{ text: prompt }]
}]
})

const req = https.request({
hostname: "generativelanguage.googleapis.com",
path: "/v1beta/models/gemini-1.5-flash:generateContent?key=" + key,
method: "POST",
headers: {
"Content-Type": "application/json"
}
}, (res)=>{

let body = ""

res.on("data", c => body += c)

res.on("end", ()=>{

try {
const json = JSON.parse(body)

const text =
json?.candidates?.[0]?.content?.parts?.[0]?.text || ""

resolve({ ok: !!text, text, raw: json })

} catch(e){
resolve({ ok:false, text:"", error:e.message })
}

})

})

req.on("error", (e)=>{
resolve({ ok:false, text:"", error:e.message })
})

req.write(data)
req.end()

})

}

module.exports = { request }
