/**
 * IMA canonical host capability negotiation.
 * Stage 6: one semantic IMA surface, many verified host adapters.
 *
 * This module only detects host capabilities. Detection never grants authority.
 */

export const IMA_HOST_CAPABILITIES = Object.freeze({
  HOST_VIEW_AVAILABLE: 'HOST_VIEW_AVAILABLE',
  HOST_WIDGET_AVAILABLE: 'HOST_WIDGET_AVAILABLE',
  IMA_RENDER_AVAILABLE: 'IMA_RENDER_AVAILABLE',
  DEVICE_VIEW_AVAILABLE: 'DEVICE_VIEW_AVAILABLE',
  DEVICE_CONTROL_AVAILABLE: 'DEVICE_CONTROL_AVAILABLE',
  END_TO_END_VERIFIED: 'END_TO_END_VERIFIED',
});

export function detectImaHostCapabilities(env = globalThis) {
  const hasOpenAIHostBridge =
    !!env?.openai &&
    typeof env.openai.callTool === 'function';

  const isChatGPTHost =
    typeof env?.location?.hostname === 'string' &&
    /(^|\.)chatgpt\.com$|(^|\.)chat\.openai\.com$/.test(env.location.hostname);

  const isImaWeb =
    typeof env?.location?.hostname === 'string' &&
    /(^|\.)imaosglobal\.github\.io$/.test(env.location.hostname);

  return Object.freeze({
    host: isChatGPTHost ? 'chatgpt' : isImaWeb ? 'ima-web' : 'unknown',
    HOST_VIEW_AVAILABLE: false,
    HOST_WIDGET_AVAILABLE: isChatGPTHost && hasOpenAIHostBridge,
    IMA_RENDER_AVAILABLE: true,
    DEVICE_VIEW_AVAILABLE: false,
    DEVICE_CONTROL_AVAILABLE: false,
    END_TO_END_VERIFIED: false,
    controlAuthority: 'separate-authorization-required',
    screenShareImpliesControl: false,
    detectionOnly: true,
  });
}

export const IMA_HOST_ADAPTERS = Object.freeze({
  chatgptMobileScreenShare: {
    mode: 'host-view',
    authority: 'view-only-unless-separately-authorized',
    activate: 'host-controlled',
  },
  chatgptMcpAppsWeb: {
    mode: 'interactive-widget',
    authority: 'mcp-tool-plus-device-authorization',
    activate: 'capability-negotiation',
  },
  imaWebPwa: {
    mode: 'interactive-web',
    authority: 'ima-device-authorization',
    activate: 'capability-negotiation',
  },
  futureHosts: {
    mode: 'capability-negotiation',
    authority: 'never-inferred',
    activate: 'detect-verify-authorize',
  },
});

export const IMA_SEMANTIC_ACTIONS = Object.freeze([
  'focus',
  'select',
  'openConversation',
  'speak',
  'type',
  'navigate',
  'cancel',
  'back',
  'help',
]);

export const IMA_SCREEN_CONTROL_CONTRACT = Object.freeze([
  'view',
  'identify',
  'authorize',
  'act',
  'observe',
  'refresh',
]);
