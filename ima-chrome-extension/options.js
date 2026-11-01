const enabled = document.getElementById("enabled");
const endpoint = document.getElementById("endpoint");
const token = document.getElementById("token");
const status = document.getElementById("status");

(async () => {
  const s = await chrome.storage.local.get({ enabled: true, endpoint: "", token: "" });
  enabled.checked = s.enabled;
  endpoint.value = s.endpoint;
  token.value = s.token;
})();

document.getElementById("save").addEventListener("click", async () => {
  await chrome.storage.local.set({
    enabled: enabled.checked,
    endpoint: endpoint.value.trim(),
    token: token.value
  });
  status.textContent = "Saved.";
});
