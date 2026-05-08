const fs=require('fs');
const cp=require('child_process');
const path=require('path');
const crypto=require('crypto');

const ROOT=process.cwd();

function run(cmd){
  try{
    return cp.execSync(cmd,{
      cwd:ROOT,
      shell:true,
      stdio:'pipe'
    }).toString().trim();
  }catch(e){
    return null;
  }
}

// ---------------- HASH ----------------

function fileHash(file){
  return crypto.createHash('sha256')
    .update(fs.readFileSync(file))
    .digest('hex');
}

// ---------------- SCAN ----------------

function scan(dir){

  const files=[];
  const hashes=new Map();
  const broken=[];
  const duplicates=[];
  const unused=[];

  function walk(d){

    for(const f of fs.readdirSync(d)){

      const full=path.join(d,f);
      const rel=path.relative(ROOT,full);

      if(rel.includes('node_modules') || rel.includes('.git')) continue;

      const stat=fs.statSync(full);

      if(stat.isDirectory()){
        walk(full);
        continue;
      }

      files.push(rel);

      try{

        const h=fileHash(full);

        if(!hashes.has(h)) hashes.set(h,[]);
        hashes.get(h).push(rel);

      }catch(e){
        broken.push(rel);
      }
    }
  }

  walk(dir);

  for(const [h,list] of hashes){
    if(list.length>1) duplicates.push(list);
  }

  return {files,broken,duplicates};
}

// ---------------- CHECK EXECUTION ----------------

function checkSyntax(file){
  return run(`node --check "${file}"`);
}

// ---------------- BUILD CLEAN PROJECT ----------------

function buildClean(scanResult){

  const outDir='build_clean';

  fs.rmSync(outDir,{recursive:true,force:true});
  fs.mkdirSync(outDir,{recursive:true});

  for(const f of scanResult.files){

    const src=path.join(ROOT,f);
    const dst=path.join(ROOT,outDir,f);

    fs.mkdirSync(path.dirname(dst),{recursive:true});

    fs.copyFileSync(src,dst);
  }

  return outDir;
}

// ---------------- MAIN ----------------

console.log("IMA MAINTENANCE ENGINE START");

const backupDir=`backups/maintenance_${Date.now()}`;
fs.mkdirSync(backupDir,{recursive:true});

run(`cp -r . ${backupDir} || true`);

const scanResult=scan(ROOT);

console.log("FILES:",scanResult.files.length);
console.log("BROKEN:",scanResult.broken.length);
console.log("DUPLICATES:",scanResult.duplicates.length);

// syntax validation
const invalid=[];

for(const f of scanResult.files){

  if(f.endsWith('.js')){

    const ok=checkSyntax(f);

    if(ok===null){
      invalid.push(f);
    }

  }
}

// report
fs.writeFileSync(
  'logs/maintenance_report.json',
  JSON.stringify({
    broken:scanResult.broken,
    duplicates:scanResult.duplicates,
    invalid
  },null,2)
);

// build clean
const cleanDir=buildClean(scanResult);

console.log("CLEAN BUILD CREATED:",cleanDir);

// git snapshot
run('git add .');
run(`git commit -m "maintenance snapshot" || true`);
run('git push || true');

console.log("MAINTENANCE COMPLETE");
