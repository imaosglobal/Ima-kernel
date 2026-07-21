const events = require('./ima_events');
const sync = require('./ima_sync');

function react(event, handler){
  events.on(event, (data)=>{
    const result = handler(data, sync.dump());
    if(result && typeof result === 'object'){
      Object.entries(result).forEach(([k,v])=>{
        sync.set(k,v);
      });
    }
  });
}

module.exports = { react };
