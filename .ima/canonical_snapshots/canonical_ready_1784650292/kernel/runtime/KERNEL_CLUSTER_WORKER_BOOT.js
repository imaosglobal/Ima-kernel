console.log('[WORKER BOOT]', process.pid);

process.on('uncaughtException',(e)=>{
  console.error('[WORKER ERROR]',e);
});

process.on('unhandledRejection',(e)=>{
  console.error('[WORKER REJECTION]',e);
});

process.on('message',(msg)=>{

  console.log('[WORKER MESSAGE]',msg);

  if(process.send){

    process.send({
      session:msg.session,
      nodeId:msg.nodeId,
      cmd:msg.cmd
    });

  }

});

setInterval(()=>{

  console.log('[WORKER HEARTBEAT]',process.pid);

},3000);
