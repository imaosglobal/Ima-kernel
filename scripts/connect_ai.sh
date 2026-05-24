#!/data/data/com.termux/files/usr/bin/bash

echo "[SYNC] starting"

read -p "Gemini API Key: " APIKEY

export GEMINI_API_KEY="$APIKEY"

cd ~/ima_kernel || exit

node <<'NODE'
const { handle } =
require("./kernel/vibe/termux_gateway")

async function run(){

  const res = await handle(
    "build autonomous sync layer for IMA kernel"
  )

  console.log("[FINAL RESULT]")
  console.log(res)

}

run()
NODE
