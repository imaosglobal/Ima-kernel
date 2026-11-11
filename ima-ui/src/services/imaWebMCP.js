import { useEffect } from 'react';

const WEBMCP_TOOLSET_VERSION = '1.1.0';

function validateNavigationTarget(value) {
  const parsed = new URL(value);
  if (!['https:', 'http:'].includes(parsed.protocol)) return { ok: false, error: 'unsupported_protocol' };
  if (parsed.username || parsed.password) return { ok: false, error: 'embedded_credentials_forbidden' };
  if (parsed.protocol === 'http:' && !['localhost', '127.0.0.1', '[::1]'].includes(parsed.hostname)) return { ok: false, error: 'insecure_http_requires_loopback' };
  return { ok: true, url: parsed.toString() };
}
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
    description: 'Navigate the connected local Chrome workspace to a user-authorized HTTPS URL, or HTTP on loopback only. Navigation is consequential and page content is untrusted.',
    inputSchema: {
      type: 'object',
      properties: { url: { type: 'string', description: 'Destination URL.' } },
      required: ['url'],
      additionalProperties: false
    },
    annotations: { consequentialHint: true, untrustedContentHint: true },
    execute: async ({ url }) => {
      try {
        const target = validateNavigationTarget(url);
        if (!target.ok) return target;
        const result = await localNavigate(target.url);
        return { ok: true, result, toolsetVersion: WEBMCP_TOOLSET_VERSION };
      } catch (error) {
        return { ok: false, error: String(error?.message || error) };
      }
    }
  }
];

export async function registerImaWebMCP(signal) {
  if (!window.isSecureContext) return {ok:false,reason:'insecure_context',message:'WebMCP requires HTTPS.'};
  const modelContext = document.modelContext;
  if (!modelContext) return {ok:false,reason:'webmcp_unavailable',message:'Native WebMCP is not available; use IMA browser bridge fallback.'};
  try {
    const registered=[];
    for (const tool of tools) { await modelContext.registerTool(tool, signal ? { signal } : undefined); registered.push(tool.name); }
    return {ok:true,tools:registered,toolsetVersion:WEBMCP_TOOLSET_VERSION,message:`${registered.length} IMA browser tools registered.`};
  } catch(error){ return {ok:false,reason:'registration_failed',message:String(error?.message||error)}; }
}

export function useImaWebMCP(enabled = true) {
  useEffect(() => {
    if (!enabled || !window.isSecureContext || !document.modelContext) return;
    const controller = new AbortController();
    let active = true;
    (async () => { try { if (active) await registerImaWebMCP(controller.signal); } catch { /* registration is optional; fallback remains available */ } })();
    return () => {
      active = false;
      controller.abort();
    };
  }, [enabled]);
}
