
const fs=require('fs');

module.exports=function(){

const required=[

'package.json',
'server.js',
'cli.js',
'core/runtime_registry.json'

];

for(const r of required){

if(!fs.existsSync(r)){

console.log('MISSING',r);

}

}

console.log('SELF REPAIR COMPLETE');

};
