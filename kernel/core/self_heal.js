
const fs=require('fs');

module.exports=function(){

const required=[
'server.js',
'package.json',
'cli.js',
'ui/index.html'
];

for(const f of required){

if(!fs.existsSync(f)){

console.log('MISSING',f);

}

}

};
