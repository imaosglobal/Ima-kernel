const fs = require('fs');

let f = fs.readFileSync('ima_engine_final.js','utf8');

// מחליף כל פונקציית npmPublish
f = f.replace(/function npmPublish[\s\S]*?\}/, `
function npmPublish(){
  const { execSync } = require('child_process');

  console.log('\\n[NPM]');

  try {
    execSync('npm publish', {stdio:'inherit'});
    console.log('[NPM] published');
    return true;
  } catch(e){
    console.log('[NPM] already exists or failed safely');
    return false;
  }
}
`);

fs.writeFileSync('ima_engine_final.js', f);
console.log('[FIXED npmPublish]');
