const { setKeys, show, test } = require("./kernel/cli/keyvault")

const cmd = process.argv[2]

if(cmd === "set") setKeys()
else if(cmd === "show") show()
else if(cmd === "test") test()
else console.log("usage: node keyctl.js set|show|test")
