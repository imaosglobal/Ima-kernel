
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

return res.end(
JSON.stringify({

status:'online',
time:Date.now()

})

);

}

res.end('IMA');

}).listen(4000,()=>{

console.log('IMA ONLINE 4000');

});
