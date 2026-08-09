const {
  default: makeWASocket,
  useMultiFileAuthState,
  fetchLatestBaileysVersion,
  DisconnectReason
} = require('../whatsapp_bridge/node_modules/@whiskeysockets/baileys');

const pino = require('../whatsapp_bridge/node_modules/pino');
const path = require('path');
const fs = require('fs');

const phone = process.env.WA_PAIRING_PHONE;

if (!phone) {
  console.log('ERROR: WA_PAIRING_PHONE is missing');
  process.exit(1);
}

const auth = path.resolve('.ima/wa_pairing_test');
fs.mkdirSync(auth, { recursive: true });

let version;
let attempts = 0;
let pairingRequested = false;

async function start() {
  attempts++;

  const { state, saveCreds } = await useMultiFileAuthState(auth);

  if (state.creds.registered) {
    console.log('ALREADY_REGISTERED');
  }

  try {
    const latest = await fetchLatestBaileysVersion();
    version = latest.version;
    console.log('WA_VERSION:', version);
  } catch (e) {
    console.log('WA_VERSION_FETCH_FAILED:', e.message);
  }

  const sock = makeWASocket({
    ...(version ? { version } : {}),
    auth: state,
    logger: pino({ level: 'silent' }),
    browser: ['IMA', 'Chrome', '1.0.0']
  });

  sock.ev.on('creds.update', saveCreds);

  let pairingTimer = null;

  const requestPairing = async () => {
    if (pairingRequested || state.creds.registered) return;

    pairingRequested = true;

    try {
      console.log('PAIRING_REQUEST_START');

      const code = await sock.requestPairingCode(phone);

      console.log('==============================');
      console.log('WHATSAPP_PAIRING_CODE:', code);
      console.log('==============================');
      console.log('ACTION: WhatsApp > Linked devices > Link a device > Link with phone number');
      console.log('WAITING_FOR_WHATSAPP_LINK...');
    } catch (e) {
      pairingRequested = false;
      console.log('PAIRING_ERROR:', e.message);
    }
  };

  sock.ev.on('connection.update', async update => {
    const { connection, qr, lastDisconnect } = update;

    console.log(
      'CONNECTION:',
      connection || 'connecting',
      'QR:',
      !!qr
    );

    /*
     * Do NOT wait for "open".
     * Pairing must be requested while the socket is still usable.
     */
    if (
      !state.creds.registered &&
      !pairingRequested &&
      !pairingTimer
    ) {
      pairingTimer = setTimeout(() => {
        requestPairing();
      }, 1500);
    }

    if (connection === 'open') {
      console.log('WHATSAPP_CONNECTED');
      console.log('PAIRING_TEST_SUCCESS');
      return;
    }

    if (connection === 'open') {
      if (pairingTimer) {
        clearTimeout(pairingTimer);
        pairingTimer = null;
      }

      pairingRequested = false;

      console.log('================================');
      console.log('WHATSAPP_CONNECTED');
      console.log('PAIRING_SUCCESS');
      console.log('IMA_WHATSAPP_READY');
      console.log('================================');

      return;
    }

    if (connection === 'close') {
      if (pairingTimer) {
        clearTimeout(pairingTimer);
        pairingTimer = null;
      }

      const code =
        lastDisconnect?.error?.output?.statusCode;

      console.log('CLOSED_CODE:', code ?? 'unknown');

      if (code === DisconnectReason.loggedOut) {
        console.log('WHATSAPP_LOGGED_OUT');
        process.exit(3);
      }

      console.log('RECONNECT_REQUIRED');

      pairingRequested = false;

      setTimeout(() => {
        console.log('RECONNECTING_ATTEMPT:', attempts + 1);
        start();
      }, 2000);
    }
  });
}

console.log('IMA WHATSAPP PAIRING TEST');
console.log('PHONE:', phone);
console.log('AUTH:', auth);

start().catch(e => {
  console.log('FATAL:', e.message);
  process.exit(1);
});
