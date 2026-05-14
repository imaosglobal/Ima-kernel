const fs = require("fs");
const path = require("path");

const ROOT = process.env.HOME + "/ima_kernel";

const KEEP = [
  "core",
  "runtime",
  "ui",
  "archive",
  "logs",
  "ima.js",
  "package.json"
];

console.log("=== IMA REBUILDER START ===");

// -------------------------
// ENSURE CLEAN STRUCTURE
// -------------------------
["core","runtime","ui","archive","logs"]
.forEach(d=>{
  fs.mkdirSync(path.join(ROOT,d),{recursive:true});
});

// -------------------------
// MOVE EVERYTHING ELSE
// -------------------------
const items = fs.readdirSync(ROOT);

for(const item of items){

  if(KEEP.includes(item)) continue;

  const src = path.join(ROOT,item);
  const dst = path.join(ROOT,"archive",item);

  try{

    fs.renameSync(src,dst);

    console.log("ARCHIVED:",item);

  }catch(e){

    console.log("SKIP:",item);

  }

}

// -------------------------
// BUILD SINGLE CORE
// -------------------------
const core = `
const express = require("express");
const app = express();

app.use(express.json());

const MEMORY=[];

app.get("/health",(_,res)=>{
  res.json({
    ok:true,
    mode:"IMA_SINGLE_CORE",
    ts:Date.now()
  });
});

app.get("/memory",(_,res)=>{
  res.json(MEMORY);
});

app.post("/memory",(req,res)=>{
  MEMORY.push(req.body||{});
  res.json({ok:true});
});

app.get("/",(_,res)=>{
  res.send("IMA SINGLE CORE ONLINE");
});

app.listen(3000,()=>{
  console.log("IMA CORE ONLINE 3000");
});
`;

fs.writeFileSync(ROOT+"/ima.js",core);

// -------------------------
// PACKAGE
// -------------------------
fs.writeFileSync(
  ROOT+"/package.json",
  JSON.stringify({
    name:"ima-kernel",
    version:"rebuilt",
    main:"ima.js",
    scripts:{
      start:"node ima.js"
    },
    dependencies:{
      express:"latest"
    }
  },null,2)
);

// -------------------------
// FINAL STATE
// -------------------------
fs.writeFileSync(
  ROOT+"/core/rebuild_state.json",
  JSON.stringify({
    rebuilt:true,
    ts:Date.now()
  },null,2)
);

console.log("=== REBUILD COMPLETE ===");
