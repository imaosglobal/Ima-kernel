const { sendToCloud } = require("../cloud/cloud_bridge")

async function vibe(input){

console.log("[VIBE INPUT]", input)

const cloud = await sendToCloud(input)

console.log("[CLOUD]", cloud)

if(
cloud &&
cloud !== "[EMPTY_RESPONSE]" &&
cloud !== "[PARSE_ERROR]" &&
cloud !== "[REQUEST_FAILED]"
){
return {
type: "cloud",
output: cloud
}
}

return {
type: "text",
output: cloud
}

}

module.exports = { vibe }
