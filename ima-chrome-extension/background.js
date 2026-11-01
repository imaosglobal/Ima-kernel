const DEFAULTS = {
  enabled: true,
  endpoint: "",
  token: ""
};

async function getSettings() {
  return chrome.storage.local.get(DEFAULTS);
}

chrome.runtime.onInstalled.addListener(async () => {
  const current = await chrome.storage.local.get(DEFAULTS);
  await chrome.storage.local.set({ ...DEFAULTS, ...current });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    if (message?.type === "GET_STATE") {
      sendResponse({ ok: true, settings: await getSettings() });
      return;
    }

    if (message?.type === "RUN_PAGE_READ") {
      const settings = await getSettings();
      if (!settings.enabled) throw new Error("IMA Browser Bridge is disabled.");

      const tabId = message.tabId ?? sender.tab?.id;
      if (!Number.isInteger(tabId)) throw new Error("No active tab.");

      const [result] = await chrome.scripting.executeScript({
        target: { tabId },
        func: () => ({
          url: location.href,
          title: document.title,
          text: document.body?.innerText?.slice(0, 20000) || "",
          timestamp: new Date().toISOString()
        })
      });

      const payload = result?.result ?? {};
      await chrome.storage.local.set({ lastResult: payload });

      if (settings.endpoint) {
        await sendToIma(settings, payload);
      }

      sendResponse({ ok: true, result: payload });
      return;
    }

    if (message?.type === "OPEN_LINK") {
      const url = new URL(message.url);
      if (!["http:", "https:"].includes(url.protocol)) {
        throw new Error("Only HTTP(S) links are allowed.");
      }
      await chrome.tabs.create({ url: url.href, active: true });
      sendResponse({ ok: true });
      return;
    }

    throw new Error("Unknown message.");
  })().catch(error => sendResponse({ ok: false, error: String(error.message || error) }));

  return true;
});

async function sendToIma(settings, payload) {
  const headers = { "Content-Type": "application/json" };
  if (settings.token) headers.Authorization = `Bearer ${settings.token}`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(settings.endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify({
        source: "ima-chrome-extension",
        version: "0.1.0",
        event: "PAGE_READ",
        payload
      }),
      signal: controller.signal
    });
    if (!response.ok) throw new Error(`IMA endpoint returned HTTP ${response.status}`);
  } finally {
    clearTimeout(timeout);
  }
}
