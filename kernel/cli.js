#!/usr/bin/env node

const http=require('http');

const cmd=process.argv[2]||'status';

const host=process.env.IMA_HOST||'localhost';

const port=process.env.IMA_PORT||4000;

http.get(
'http://'+host+':'+port+'/'+cmd,
res=>res.pipe(process.stdout)
).on(
'error',
()=>{
console.log('IMA OFFLINE');
}
);
