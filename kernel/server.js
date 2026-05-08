
const http=require('http');
const fs=require('fs');

http.createServer((req,res)=>{

if(req.url==='/'){

res.writeHead(200,{
'content-type':'text/html'
});

return res.end(
fs.readFileSync('./ui/index.html')
);

}

if(req.url==='/status'){

return res.end('IMA ONLINE');

}

res.end('OK');

}).listen(4000,()=>{

console.log('IMA RUNNING ON 4000');

});
