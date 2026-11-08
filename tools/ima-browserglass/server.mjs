import http from 'node:http';
import { spawn } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import httpProxy from 'http-proxy';
const { createProxyServer } = httpProxy;

const PORT = Number(process.env.PORT || 10000);
const BGLS_PORT = Number(process.env.BGLS_INTERNAL_PORT || 7799);
const BGLS_DIR = process.env.BGLS_HOME || '/opt/browserglass';
const DATA_DIR = process.env.BGLS_DATA_DIR || '/opt/browserglass/bgls-data';
const CHROME_BIN = process.env.CHROME_BIN || '/usr/bin/chromium';
const EMBED_ORIGIN = 'https://imaosglobal.github.io';
const EMBED_COOKIE = 'ima_browserglass_embed';

let gateway;
let instanceId = null;
let targetId = null;
let lastToken = null;
let lastTokenExpiresAt = 0;

function run(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: { ...process.env, ...options.env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', d => { stdout += d; });
    child.stderr.on('data', d => { stderr += d; });
    child.on('error', reject);
    child.on('close', code => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`${command} exited ${code}: ${stderr || stdout}`));
    });
  });
}

async function waitForGateway() {
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`http://127.0.0.1:${BGLS_PORT}/browserglass/v1/instances`, { method: 'GET' });
      if (r.status !== 404) return;
    } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error('BrowserGlass gateway did not become ready');
}

async function adminToken() {
  const r = await run('pnpm', ['-s', 'bgls', 'token', '--ttl', '900'], { cwd: BGLS_DIR });
  return r.stdout.trim();
}

async function ensureInstance() {
  if (instanceId && targetId) return;
  const admin = await adminToken();
  const created = await fetch(`http://127.0.0.1:${BGLS_PORT}/browserglass/v1/instances`, {
    method: 'POST',
    headers: { authorization: `Bearer ${admin}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      requestId: `ima-live-${Date.now()}`,
      browser: { headless: 'new', executablePath: CHROME_BIN },
    }),
  });
  if (!created.ok) throw new Error(`BrowserGlass instance creation failed: ${created.status} ${await created.text()}`);
  const data = await created.json();
  instanceId = data.instanceId;

  const targets = await fetch(`http://127.0.0.1:${BGLS_PORT}/browserglass/v1/instances/${instanceId}/targets`, {
    headers: { authorization: `Bearer ${admin}` },
  });
  if (!targets.ok) throw new Error(`BrowserGlass target discovery failed: ${targets.status}`);
  const td = await targets.json();
  targetId = td.targets?.[0]?.targetId || td[0]?.targetId;
  if (!targetId) throw new Error('BrowserGlass returned no target');
}

async function mintViewerToken() {
  await ensureInstance();
  if (lastToken && Date.now() < lastTokenExpiresAt - 30000) return lastToken;
  const admin = await adminToken();
  const r = await fetch(`http://127.0.0.1:${BGLS_PORT}/browserglass/v1/tokens`, {
    method: 'POST',
    headers: { authorization: `Bearer ${admin}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      sub: 'ima-live-browser-viewer',
      subKind: 'service',
      scope: { kind: 'instance', instanceId, targets: '*' },
      caps: ['view', 'control', 'navigate', 'automation'],
      ttlSeconds: 300,
    }),
  });
  if (!r.ok) throw new Error(`BrowserGlass token mint failed: ${r.status} ${await r.text()}`);
  const data = await r.json();
  lastToken = data.token;
  lastTokenExpiresAt = Number(data.expiresAt || Date.now() + 240000);
  return lastToken;
}

const gatewayProcess = spawn('node', [
  `${BGLS_DIR}/packages/cli/dist/bin.mjs`, 'serve',
  '--listen', `127.0.0.1:${BGLS_PORT}`,
], {
  cwd: BGLS_DIR,
  env: { ...process.env, CHROME_BIN, BGLS_CHROME_PATH: CHROME_BIN, BGLS_DATA_DIR: DATA_DIR },
  stdio: ['ignore', 'pipe', 'pipe'],
});
gatewayProcess.stdout.on('data', d => process.stdout.write(`[browserglass] ${d}`));
gatewayProcess.stderr.on('data', d => process.stderr.write(`[browserglass] ${d}`));
gatewayProcess.on('exit', code => {
  if (code !== 0) process.stderr.write(`[browserglass] gateway exited: ${code}\n`);
});

const proxy = createProxyServer({
  target: `http://127.0.0.1:${BGLS_PORT}`,
  ws: true,
  changeOrigin: true,
});

proxy.on('error', (err, req, res) => {
  if (res && !res.headersSent) {
    res.writeHead(502, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'browserglass_gateway_unavailable', detail: err.message }));
  }
});

const server = http.createServer(async (req, res) => {
  try {
    const cookieHeader = String(req.headers.cookie || '');
    const hasEmbedCookie = cookieHeader.split(';').some(v => v.trim().startsWith(EMBED_COOKIE + '='));
    const referer = String(req.headers.referer || '');
    if (req.url === '/' && referer.startsWith(EMBED_ORIGIN + '/')) {
      res.setHeader('Set-Cookie', `${EMBED_COOKIE}=1; Path=/; Secure; HttpOnly; SameSite=None; Max-Age=86400`);
    }

    if (req.url === '/healthz') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ ok: true, service: 'ima-browserglass' }));
      return;
    }

    if (req.url === '/api/session') {
      if (!hasEmbedCookie) {
        res.writeHead(403, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ error: 'IMA embed required' }));
        return;
      }
      const token = await mintViewerToken();
      const wsProtocol = req.headers['x-forwarded-proto'] === 'https' ? 'wss' : 'ws';
      const host = req.headers.host;
      res.writeHead(200, {
        'content-type': 'application/json',
        'cache-control': 'no-store',
      });
      res.end(JSON.stringify({
        url: `${wsProtocol}://${host}/browserglass/socket`,
        token,
        targetId,
        expiresAt: lastTokenExpiresAt,
      }));
      return;
    }

    if (req.url === '/') {
      const html = await readFile(new URL('./viewer.html', import.meta.url), 'utf8');
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' });
      res.end(html);
      return;
    }

    if (req.url === '/browserglass-embed.global.js') {
      const js = await readFile('/opt/browserglass/packages/embed/dist/browserglass-embed.global.js');
      res.writeHead(200, { 'content-type': 'application/javascript', 'cache-control': 'public, max-age=3600' });
      res.end(js);
      return;
    }

    if (req.url?.startsWith('/browserglass/')) {
      proxy.web(req, res);
      return;
    }

    res.writeHead(404);
    res.end('not found');
  } catch (err) {
    res.writeHead(500, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'browserglass_service_error', detail: err.message }));
  }
});

server.on('upgrade', (req, socket, head) => {
  const cookieHeader = String(req.headers.cookie || '');
  const hasEmbedCookie = cookieHeader.split(';').some(v => v.trim().startsWith(EMBED_COOKIE + '='));
  if (req.url?.startsWith('/browserglass/') && hasEmbedCookie) proxy.ws(req, socket, head);
  else socket.destroy();
});

server.listen(PORT, '0.0.0.0', async () => {
  try {
    await waitForGateway();
    console.log('IMA BrowserGlass gateway ready');
  } catch (err) {
    console.error(`IMA BrowserGlass gateway readiness warning: ${err.message}`);
  }
  console.log(`IMA BrowserGlass service listening on :${PORT}`);
});

process.on('SIGTERM', () => gatewayProcess.kill('SIGTERM'));
process.on('SIGINT', () => gatewayProcess.kill('SIGINT'));
