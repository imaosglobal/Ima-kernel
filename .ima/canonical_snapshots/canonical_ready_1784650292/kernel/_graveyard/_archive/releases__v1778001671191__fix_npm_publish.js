const fs = require('fs');

let f = fs.readFileSync('ima_engine_final.js','utf8');

f = f.replace(/function npmPublish[\s\S]*?\}/, `

function npmPublish(){
  const { execSync } = require('child_process');

  try {
    console.log('\\n[NPM]');

    const pkg = JSON.parse(require('fs').readFileSync('package.json'));
    const name = pkg.name;

    // מביא גרסה אחרונה מ-npm
    let latest = '0.0.0';
    try {
      latest = execSync(\`npm view \${name} version\`, {encoding:'utf8'}).trim();
    } catch(e){}

    const parts = latest.split('.').map(Number);
    parts[2] += 1;

    const next = parts.join('.');

    execSync(\`npm version \${next} --no-git-tag-version\`, {stdio:'inherit'});
    execSync('npm publish',{stdio:'inherit'});

    console.log('[NPM] published', next);

  } catch(e){
    console.log('[NPM] publish failed:', e.message);
  }
}
`);

fs.writeFileSync('ima_engine_final.js', f);
console.log('[NPM FIX APPLIED]');
