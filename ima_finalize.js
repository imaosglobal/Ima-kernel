const fs = require("fs");
const path = require("path");

const ROOT = process.env.HOME + "/ima_kernel";

console.log("=== IMA FINALIZE ===");

// ------------------------
// WRITE FINAL RUNTIME
// ------------------------
const runtime = `
const express = require("express");
const app = express();

app.use(express.json());

const MEMORY=[];

// HEALTH
app.get("/health",(_,res)=>{
  res.json({
    ok:true,
    mode:"FINAL_SINGLE_SYSTEM",
    ts:Date.now()
  });
});

// MEMORY
app.get("/memory",(_,res)=>{
  res.json(MEMORY);
});

app.post("/memory",(req,res)=>{
  MEMORY.push(req.body||{});
  res.json({ok:true});
});

// ROOT
app.get("/",(_,res)=>{
  res.send("IMA FINAL SYSTEM ONLINE");
});

// START
app.listen(3000,()=>{
  console.log("IMA FINAL ONLINE 3000");
});
`;

fs.writeFileSync(
  ROOT + "/ima.js",
  runtime
);

// ------------------------
// FINAL STATE
// ------------------------
fs.writeFileSync(
  ROOT + "/core/final_state.json",
  JSON.stringify({
    mode:"FINAL",
    archiveIgnored:true,
    ts:Date.now()
  },null,2)
);

console.log("FINAL SYSTEM READY");
