const engine = require("./runtime/engine");
const sync = require("./runtime/autonomous_sync");

function register(app){

  app.get("/health",(req,res)=>{
    res.json({ ok:true, system:"IMA_AUTONOMOUS_SYNC" });
  });

  app.get("/engine",(req,res)=>{
    res.json(engine.status());
  });

  app.get("/modules",(req,res)=>{
    res.json(engine.status().modules);
  });

  app.post("/sync/cycle",(req,res)=>{
    res.json(sync.cycle());
  });

}

module.exports = { register };
