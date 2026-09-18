import { useEffect, useState } from 'react';

const INITIAL = {
  status: 'connecting', source: 'IMA runtime', updatedAt: null,
  memory: { available: false, records: 0 },
  learning: { available: false, records: 0 },
  agents: ['ChatGPT', 'Claude', 'Gemini'], error: null,
};

async function readRuntime() {
  const response = await fetch('/ima-api/runtime', { cache: 'no-store' });
  if (!response.ok) throw new Error(`runtime HTTP ${response.status}`);
  return response.json();
}

export function useImaRuntime(intervalMs = 10000) {
  const [state, setState] = useState(INITIAL);
  useEffect(() => {
    let alive = true;
    const sync = async () => {
      try {
        const next = await readRuntime();
        if (alive) setState({ ...INITIAL, ...next, status: 'active', error: null });
      } catch (error) {
        if (alive) setState(prev => ({ ...prev, status: 'unavailable', error: error.message }));
      }
    };
    sync();
    const timer = setInterval(sync, intervalMs);
    return () => { alive = false; clearInterval(timer); };
  }, [intervalMs]);
  return state;
}
