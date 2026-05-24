const fs = require("fs")
const path = require("path")
const readline = require("readline")

const VAULT = path.join(process.env.HOME, "ima_kernel/kernel/cloud/keys.vault.json")

function load(){
  try { return JSON.parse(fs.readFileSync(VAULT,"utf8")) }
  catch(e){ return {} }
}

function save(data){
  fs.writeFileSync(VAULT, JSON.stringify(data,null,2))
}

async function prompt(q){
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  })

  return new Promise(res=>{
    rl.question(q, ans=>{
      rl.close()
      res(ans)
    })
  })
}

async function setKeys(){
  const primary = await prompt("PRIMARY KEY: ")
  const secondary = await prompt("SECONDARY KEY: ")

  save({
    primary,
    secondary,
    updated: Date.now()
  })

  console.log("[VAULT] keys saved")
}

function show(){
  console.log(load())
}

async function test(){
  const keys = load()
  console.log("[VAULT TEST]", Object.keys(keys))
}

module.exports = { setKeys, show, test }
