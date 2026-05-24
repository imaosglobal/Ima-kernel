const https = require("https")

async function sendToCloud(prompt){

return new Promise((resolve,reject)=>{

const API_KEY = process.env.GEMINI_API_KEY

if(!API_KEY){
  console.log("[CLOUD] missing api key")
  return resolve("[NO_API_KEY]")
}

const body = JSON.stringify({
  contents: [
    {
      parts: [
        { text: prompt }
      ]
    }
  ]
})

const req = https.request({
  hostname: "generativelanguage.googleapis.com",
  path: "/v1beta/models/gemini-1.5-flash:generateContent?key=" + API_KEY,
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body)
  }
}, (res)=>{

  let data = ""

  res.on("data", chunk => {
    data += chunk
  })

  res.on("end", ()=>{

    try {

      console.log("[CLOUD RAW]", data)

      const json = JSON.parse(data)

      const text =
        json?.candidates?.[0]?.content?.parts?.[0]?.text

      if(!text){
        console.log("[CLOUD] empty")
        return resolve("[EMPTY_RESPONSE]")
      }

      resolve(text)

    } catch(err){

      console.log("[CLOUD ERROR]", err.message)
      resolve("[PARSE_ERROR]")

    }

  })

})

req.on("error",(err)=>{
  console.log("[HTTPS ERROR]", err.message)
  resolve("[REQUEST_FAILED]")
})

req.write(body)
req.end()

})

}

module.exports = { sendToCloud }
