const readline = require("readline")
const { save } = require("./kernel/cloud/key_vault")

const rl = readline.createInterface({
input: process.stdin,
output: process.stdout
})

function ask(q){

return new Promise(r=>rl.question(q,r))

}

async function run(){

console.log("[KEY SETUP] Gemini API Vault")

const p = await ask("PRIMARY KEY: ")
const s = await ask("SECONDARY KEY: ")

save(p,s)

console.log("[DONE] keys stored in vault")

rl.close()

}

run()
