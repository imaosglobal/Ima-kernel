const fs = require('fs');

const REQUIRED = [
  './ima_identity',
  './ima_unified_sync',
  './ima_network_layer',
  './ima_platform_bridge'
];

function check(){
  const missing = [];

  for (const m of REQUIRED){
    try {
      require.resolve(m);
    } catch (e){
      missing.push(m);
    }
  }

  return {
    ok: missing.length === 0,
    missing
  };
}

function assert(){
  const r = check();

  if(!r.ok){
    console.error('[DEPENDENCY ERROR]');
    console.error('Missing:', r.missing);
    process.exit(1);
  }

  console.log('[DEPENDENCY OK]');
  return true;
}

module.exports = { check, assert };
