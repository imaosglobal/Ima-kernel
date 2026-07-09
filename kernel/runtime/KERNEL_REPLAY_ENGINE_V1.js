const BUS = require('./KERNEL_EVENT_BUS_V1');
const G = require('./KERNEL_API_GATEWAY_V2');

function replay(){
  const events = BUS.all();

  const results = [];

  for(const e of events){
    try{
      // רק events של execution עוברים דרך gateway
      if(e.type === 'REQUEST'){
        const res = G.request(e.payload);
        results.push({event:e.id, res});
      }
    }catch(err){
      results.push({event:e.id, error:err.message});
    }
  }

  return {
    replayed: events.length,
    results
  };
}

module.exports = { replay };
