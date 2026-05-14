const fs = require('fs');

const CP = require('./KERNEL_CONTROL_PLANE_V2');
const PIPE = require('./KERNEL_PIPELINE');

function request(event){

  if(!event || !event.type){
    return {status:'error', reason:'missing_event'};
  }

  switch(event.type){

    case 'GET_STATE':
      try{
        return {
          status:'ok',
          data: CP.read ? CP.read() : null
        };
      }catch(e){
        return {status:'error', reason:e.message};
      }

    case 'WRITE_FILE':
      try{
        if(CP.write){
          return CP.write(event.file, event.content);
        }
        fs.writeFileSync(event.file, event.content);
        return {status:'written'};
      }catch(e){
        return {status:'error', reason:e.message};
      }

    case 'SET_VERSION':
      try{
        if(PIPE.dispatch){
          PIPE.dispatch(event);
          return {status:'routed_to_pipeline'};
        }
        return {status:'no_pipeline'};
      }catch(e){
        return {status:'error', reason:e.message};
      }

    default:
      return {status:'error', reason:'unknown_type'};
  }
}

module.exports = { request };
