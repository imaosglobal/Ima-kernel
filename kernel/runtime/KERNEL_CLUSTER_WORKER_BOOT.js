const cluster = require('cluster');

process.on('message', (msg) => {
  // פשוט מחזיר הודעות חזרה ל-master
  process.send({
    session: msg.session,
    nodeId: msg.nodeId,
    cmd: msg.cmd
  });
});
