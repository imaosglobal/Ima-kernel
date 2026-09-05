const BRIDGE_API = "/bridge-api";

export async function getBridgeHealth() {
  const r = await fetch(`${BRIDGE_API}/health`);
  if (!r.ok) throw new Error(`health ${r.status}`);
  return await r.json();
}

export async function getBridgeManifest() {
  const r = await fetch(`${BRIDGE_API}/manifest`);
  if (!r.ok) throw new Error(`manifest ${r.status}`);
  return await r.json();
}

export const CAPABILITY_LABELS = {
  project_read: "קריאת פרויקטים",
  knowledge_read: "קריאת ידע",
  memory_read: "קריאת זיכרון",
  facebook_archive_read: "ארכיון Facebook",
  android_bridge: "חיבור Android",
};
