
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
