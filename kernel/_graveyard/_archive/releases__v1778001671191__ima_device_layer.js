const sync = require('./ima_sync');

function detect(){
  const ua = process.env.USER_AGENT || 'node';
  if(ua.includes('watch')) return 'watch';
  if(ua.includes('mobile')) return 'mobile';
  if(ua.includes('tv')) return 'tv';
  return 'desktop';
}

function adapt(state){
  const device = detect();

  if(device === 'watch'){
    return { mode: 'minimal', state };
  }

  if(device === 'mobile'){
    return { mode: 'compact', state };
  }

  return { mode: 'full', state };
}

module.exports = { detect, adapt };
