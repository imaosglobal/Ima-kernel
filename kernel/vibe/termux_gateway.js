const { vibe } = require("./vibe_engine")

async function handle(input){

const result = await vibe(input)

console.log("[FINAL RESULT]")
console.log(result)

return result
}

module.exports = { handle }
