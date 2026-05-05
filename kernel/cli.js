
#!/usr/bin/env node
const cp = require('child_process');
const cmd = process.argv[2] || 'run';
cp.execSync('curl -s http://localhost:4000/' + cmd,{stdio:'inherit'});
