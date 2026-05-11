
const http=require('http');
const fs=require('fs');

http.createServer((req,res)=>{

if(req.url==='/status'){

return res.end('IMA ONLINE');

}

if(req.url==='/heartbeat'){

try{

return res.end(
fs.readFileSync(
'logs/heartbeat.json'
)
);

}catch{}

}

res.end('IMA');

}).listen(4000,()=>{

console.log('IMA SERVER ONLINE');

});
