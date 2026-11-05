import { useEffect } from 'react';
import { getLocalLiveBrowserStatus, getLocalLiveBrowserScreenshot, localNavigate } from './liveBrowserBridge';

const tools = [
  {
    name: 'ima_live_browser_status',
    description: 'Read the current IMA-connected local Chrome status. Read-only.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async () => {
      try {
        const status = await getLocalLiveBrowserStatus();
        return status || { ok: false, error: 'local_bridge_unavailable' };
      } catch (error) {
        return { ok: false, error: String(error?.message || error) };
      }
    }
  },
  {
    name: 'ima_live_browser_screenshot',
    description: 'Capture the current visible screen from the connected IMA Chrome workspace. Read-only.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async () => {
      try {
        const result = await getLocalLiveBrowserScreenshot();
        return { ok: true, mime: 'image/png', data: result?.data || null };
      } catch (error) {
        return { ok: false, error: String(error?.message || error) };
      }
    }
  },
  {
    name: 'ima_live_browser_navigate',
    description: 'Navigate the connected local Chrome workspace to a user-authorized HTTPS or HTTP URL.',
    inputSchema: {
      type: 'object',
      properties: { url: { type: 'string', description: 'Destination URL.' } },
      required: ['url'],
      additionalProperties: false
    },
    annotations: { consequentialHint: true },
    execute: async ({ url }) => {
      try {
        const parsed = new URL(url);
        if (!['http:', 'https:'].includes(parsed.protocol)) {
          return { ok: false, error: 'unsupported_protocol' };
        }
        const result = await localNavigate(parsed.toString());
        return { ok: true, result };
      } catch (error) {
        return { ok: false, error: String(error?.message || error) };
      }
    }
  }
];

export async function registerImaWebMCP() {
  if (!window.isSecureContext || !('modelContext' in document)) return {ok:false,reason:'webmcp_unavailable'};
  try { const registered=[]; for (const tool of tools) { await document.modelContext.registerTool(tool); registered.push(tool.name); } return {ok:true,tools:registered}; }
  catch(error){ return {ok:false,reason:String(error?.message||error)}; }
}

export function useImaWebMCP(enabled = true) {
  useEffect(() => {
    if (!enabled || !window.isSecureContext || !('modelContext' in document)) return;
    const controller = new AbortController();
    let active = true;
    (async () => { try { if (active) await registerImaWebMCP(); } catch {} })();
    return () => {
      active = false;
      controller.abort();
    };
  }, [enabled]);
}
