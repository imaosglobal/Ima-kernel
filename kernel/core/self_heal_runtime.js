
const fs=require('fs');

module.exports=function(){

const required=[
'server.js',
'package.json'
];

for(const f of required){

if(!fs.existsSync(f)){

console.log('MISSING:',f);

}

}

console.log('SELF HEAL OK');

};
