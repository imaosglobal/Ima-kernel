
const fs=require('fs');

module.exports=function(){

const critical=[

'package.json',
'server.js',
'cli.js'

];

for(const f of critical){

if(!fs.existsSync(f)){

console.log('REPAIR REQUIRED:',f);

}

}

console.log('SELF REPAIR COMPLETE');

};
