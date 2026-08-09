const {
  default: makeWASocket,
  useMultiFileAuthState,
  fetchLatestBaileysVersion,
  DisconnectReason
} = require('../whatsapp_bridge/node_modules/@whiskeysockets/baileys');

const pino = require('../whatsapp_bridge/node_modules/pino');
const path = require('path');
const fs = require('fs');

(async () => {
  const phone = process.env.WA_PAIRING_PHONE;

  if (!phone) {
    console.log('ERROR: WA_PAIRING_PHONE is missing');
    process.exit(1);
  }

  const auth = path.resolve('.ima/wa_pairing_test');
  fs.mkdirSync(auth, { recursive: true });

  const { state, saveCreds } = await useMultiFileAuthState(auth);

  let version;
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

  let requested = false;

  async function pairing() {
    if (requested || state.creds.registered) return;
    requested = true;

    try {
      console.log('PAIRING_REQUEST_START');

      const code = await sock.requestPairingCode(phone);

      console.log('==============================');
      console.log('WHATSAPP_PAIRING_CODE:', code);
      console.log('==============================');
      console.log('ACTION: Enter this code in WhatsApp > Linked devices');
    } catch (e) {
      requested = false;
      console.log('PAIRING_ERROR:', e.message);
    }
  }

  sock.ev.on('connection.update', async update => {
    const { connection, qr, lastDisconnect } = update;

    console.log(
      'CONNECTION:',
      connection || 'connecting',
      'QR:',
      !!qr
    );

    if (!state.creds.registered && connection === 'open') {
      await pairing();
    }

    if (connection === 'close') {
      const code =
        lastDisconnect?.error?.output?.statusCode;

      console.log('CLOSED_CODE:', code ?? 'unknown');

      if (code !== DisconnectReason.loggedOut) {
        console.log('RECONNECT_REQUIRED');
      } else {
        console.log('WHATSAPP_LOGGED_OUT');
        process.exit(3);
      }
    }

    if (connection === 'open') {
      console.log('WHATSAPP_CONNECTED');
      console.log('PAIRING_TEST_SUCCESS');
      setTimeout(() => process.exit(0), 1000);
    }
  });

  // Give WhatsApp time to establish the socket.
  setTimeout(async () => {
    if (!state.creds.registered && !requested) {
      await pairing();
    }
  }, 5000);

  console.log('WAITING_FOR_WHATSAPP_LINK...');
  console.log('The process will remain open until the device is linked.');
})();
