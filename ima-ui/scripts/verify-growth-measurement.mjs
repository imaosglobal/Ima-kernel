import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');

const analytics = await readFile(resolve(ROOT, 'ima-ui/src/services/analytics.js'), 'utf8');
const growth = await readFile(resolve(ROOT, 'docs/IMA_GLOBAL_USER_GROWTH.md'), 'utf8');

const checks = [
  ['analytics adapter', analytics.includes("ima_visit") && analytics.includes("ima_chat_completed")],
  ['anonymous identifier', analytics.includes("ima-analytics-anonymous-id")],
  ['first-party endpoint hook', analytics.includes("VITE_IMA_ANALYTICS_URL")],
  ['GA4 hook', analytics.includes("VITE_GA4_MEASUREMENT_ID")],
  ['growth contract', growth.includes('Verified unique users') && growth.includes('Returning users')],
];

for (const [name, ok] of checks) console.log(`GROWTH_CHECK ${ok ? 'PASS' : 'FAIL'} ${name}`);

if (!checks.every(([, ok]) => ok)) process.exit(1);

const configured = Boolean(process.env.VITE_IMA_ANALYTICS_URL || process.env.VITE_GA4_MEASUREMENT_ID);
console.log(`GROWTH_DATA_SOURCE ${configured ? 'CONFIGURED_IN_ENV' : 'NOT_CONFIGURED — user counts remain UNMEASURED'}`);
