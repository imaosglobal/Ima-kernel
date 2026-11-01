const status = document.getElementById("status");

function show(value) {
  status.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

document.getElementById("read").addEventListener("click", async () => {
  show("Reading...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const result = await chrome.runtime.sendMessage({ type: "RUN_PAGE_READ", tabId: tab?.id });
  if (!result?.ok) show(`Error: ${result?.error || "unknown error"}`);
  else show(result.result);
});

document.getElementById("options").addEventListener("click", () => chrome.runtime.openOptionsPage());
