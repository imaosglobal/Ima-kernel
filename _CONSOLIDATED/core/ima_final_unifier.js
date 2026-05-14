const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const HOME = process.env.HOME;
const ROOT = HOME + "/ima_workspace";

function exec(cmd,cwd=ROOT){
  try{
    return cp.execSync(cmd,{
      cwd,
      shell:true,
      encoding:"utf8",
      stdio:["ignore","pipe","ignore"]
    }).toString().trim();
  }catch{
    return null;
  }
}

function walk(dir,out=[]){
  if(!fs.existsSync(dir)) return out;

  for(const f of fs.readdirSync(dir)){
    const full = path.join(dir,f);

    if(
      full.includes("node_modules") ||
      full.includes("/.git/objects")
    ) continue;

    let stat;

    try{
      stat = fs.statSync(full);
    }catch{
      continue;
    }

    if(stat.isDirectory()){
      walk(full,out);
    }else{
      out.push(full);
    }
  }

  return out;
}

console.log("================================");
console.log("IMA FINAL UNIFIER");
console.log("================================");

// ====================================
// FIND ALL IMA ROOTS
// ====================================

const roots = fs.readdirSync(HOME)
.filter(f=>f.toLowerCase().includes("ima"))
.map(f=>path.join(HOME,f))
.filter(f=>{
  try{
    return fs.statSync(f).isDirectory();
  }catch{
    return false;
  }
});

console.log("IMA ROOTS:",roots.length);

// ====================================
// DETECT REAL GIT ROOT
// ====================================

const gitRoots=[];

for(const r of roots){

  if(fs.existsSync(path.join(r,".git"))){

    const remote = exec(
      "git remote get-url origin",
      r
    );

    gitRoots.push({
      root:r,
      remote
    });

  }

}

console.log("GIT ROOTS:",gitRoots.length);

// ====================================
// PICK CANONICAL
// ====================================

let canonical =
gitRoots.find(g=>
  g.remote &&
  g.remote.includes("imaosglobal/Ima-kernel")
);

canonical = canonical
  ? canonical.root
  : ROOT;

console.log("CANONICAL:",canonical);

// ====================================
// VERIFY NPM PACKAGE
// ====================================

let npmPkg=null;

const packageFile = path.join(canonical,"package.json");

if(fs.existsSync(packageFile)){

  try{

    const pkg = JSON.parse(
      fs.readFileSync(packageFile)
    );

    npmPkg = pkg.name || null;

  }catch{}

}

console.log("NPM PACKAGE:",npmPkg);

// ====================================
// BUILD CLEAN STRUCTURE
// ====================================

const CLEAN = [
  "core",
  "runtime",
  "ui",
  "logs",
  "memory"
];

for(const d of CLEAN){

  fs.mkdirSync(
    path.join(ROOT,d),
    {recursive:true}
  );

}

// ====================================
// COPY IMPORTANT FILES ONLY
// ====================================

const allFiles = walk(canonical);

const important = allFiles.filter(f=>

  f.endsWith(".js") ||
  f.endsWith(".json") ||
  f.endsWith(".html")

);

console.log("IMPORTANT FILES:",important.length);

for(const src of important){

  const name = path.basename(src);

  const target = path.join(ROOT,name);

  try{

    fs.copyFileSync(src,target);

  }catch{}

}

// ====================================
// WRITE TRUTH STATE
// ====================================

const state = {
  canonical,
  npmPackage:npmPkg,
  github:"https://github.com/imaosglobal/Ima-kernel",
  totalImported:important.length,
  ts:Date.now()
};

fs.writeFileSync(
  path.join(ROOT,"core/system_truth.json"),
  JSON.stringify(state,null,2)
);

// ====================================
// CONNECT GIT
// ====================================

if(!fs.existsSync(path.join(ROOT,".git"))){

  exec("git init",ROOT);

}

exec(
'git remote remove origin || true',
ROOT
);

exec(
'git remote add origin https://github.com/imaosglobal/Ima-kernel.git',
ROOT
);

// ====================================
// VERIFY
// ====================================

const remote = exec(
"git remote get-url origin",
ROOT
);

console.log("REMOTE:",remote);

// ====================================
// FINAL
// ====================================

console.log("================================");
console.log("IMA SYSTEM UNIFIED");
console.log("================================");

console.log(state);
