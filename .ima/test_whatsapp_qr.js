const { default: makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } = require('../whatsapp_bridge/node_modules/@whiskeysockets/baileys');
const pino = require('../whatsapp_bridge/node_modules/pino');
const path = require('path'); const fs = require('fs');
const auth = path.resolve('.ima/wa_qr_test'); fs.mkdirSync(auth, { recursive: true });
(async()=>{
  const { state, saveCreds } = await useMultiFileAuthState(auth);
  const { version } = await fetchLatestBaileysVersion();
  const sock = makeWASocket({ version, auth, logger: pino({ level: 'warn' }), printQRInTerminal: true, browser: ['Chrome','20.0.04'] });
  sock.ev.on('creds.update', saveCreds);
  sock.ev.on('connection.update', ({connection})=>{ console.log('CONN:',connection); if(connection==='open') console.log('IMA_READY!'); });
})();
