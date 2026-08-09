const { default: makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } = require('../whatsapp_bridge/node_modules/@whiskeysockets/baileys');
const pino = require('../whatsapp_bridge/node_modules/pino');
const path = require('path'); const fs = require('fs');
const auth = path.resolve('.ima/wa_pair'); fs.mkdirSync(auth, { recursive: true });
(async()=>{
  const { state, saveCreds } = await useMultiFileAuthState(auth);
  const { version } = await fetchLatestBaileysVersion();
  const sock = makeWASocket({ version, auth, logger: pino({ level: 'fatal' }) });
  sock.ev.on('creds.update', saveCreds);
  if (!state.creds.registered) {
    const code = await sock.requestPairingCode('972542290945');
    console.log('=== הקוד שלך לוואטסאפ ===');
    console.log(code.match(/.{1,4}/g).join('-'));
    console.log('=== לך לוואטסאפ > מכשירים מקושרים > קשר מכשיר עם מספר ===');
  }
  sock.ev.on('connection.update', ({connection})=>{ if(connection==='open') console.log('IMA_READY! מחובר!'); });
})();
