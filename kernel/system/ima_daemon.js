const fs=require('fs');
const cp=require('child_process');

function run(cmd){
  try {
    return cp.execSync(cmd,{stdio:'pipe'}).toString().trim();
  } catch(e){
    return null;
  }
}

function sleep(ms){
  return new Promise(r=>setTimeout(r,ms));
}

async function loop(){

  console.log("IMA DAEMON STARTED");

  while(true){

    try {

      // 1. sync git
      run("git pull --rebase || true");

      // 2. run pipeline
      run("node system/final_autonomous_pipeline.js");

      // 3. health check
      const ok = run("node server.js --check") !== null;

      if(!ok){
        console.log("RECOVERY MODE");
        run("node system/final_autonomous_pipeline.js");
      }

      // 4. throttle (חשוב למניעת עומס)
      await sleep(30000);

    } catch(e){
      console.log("DAEMON ERROR:", e);
      await sleep(10000);
    }

  }
}

loop();
