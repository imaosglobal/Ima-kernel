
const https=require('https');
const fs=require('fs');

function fetch(url){

return new Promise(resolve=>{

https.get(url,res=>{

let data='';

res.on('data',d=>data+=d);

res.on('end',()=>{

try{

resolve(JSON.parse(data));

}catch{

resolve(null);

}

});

}).on('error',()=>resolve(null));

});

}

(async()=>{

const pkg='@mom-os1/ima-core';

const downloads=
await fetch(
'https://api.npmjs.org/downloads/point/last-week/'+pkg
);

fs.writeFileSync(
'logs/npm_downloads.json',
JSON.stringify(downloads,null,2)
);

})();
