const POOL = require('./KERNEL_EXECUTION_POOL_V1');

POOL.start();

function validate(req) {
  if (!req || !req.type) {
    return { ok: false, reason: 'missing_type' };
  }
  return { ok: true };
}

function request(req) {
  const v = validate(req);
  if (!v.ok) {
    return { status: 'rejected', reason: v.reason };
  }

  switch (req.type) {
    case 'WRITE_FILE':
      return POOL.request(req);

    case 'GET_STATE':
      return {
        status: 'ok',
        data: POOL.metrics()
      };

    case 'INSPECT':
      return {
        status: 'ok',
        data: POOL.inspect(req.session)
      };

    default:
      return { status: 'error', reason: 'unknown_type' };
  }
}

function metrics() {
  return POOL.metrics();
}

module.exports = { request, metrics };
