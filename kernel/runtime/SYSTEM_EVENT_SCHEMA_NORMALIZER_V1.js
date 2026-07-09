function normalize(event) {
  if (!event) return null;

  const cmd = event.cmd || event;

  return {
    session: cmd.session || event.session || 'legacy',
    nodeId: cmd.nodeId || event.nodeId || event.id || generateId(event),
    cmd: {
      type: cmd.type,
      file: cmd.file,
      content: cmd.content
    },
    raw: event
  };
}

function generateId(obj) {
  return require('crypto')
    .createHash('sha1')
    .update(JSON.stringify(obj))
    .digest('hex');
}

module.exports = { normalize };
