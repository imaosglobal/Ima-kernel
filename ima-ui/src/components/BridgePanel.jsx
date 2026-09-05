import { useEffect, useState } from "react";
import {
  getBridgeHealth,
  getBridgeManifest,
  CAPABILITY_LABELS,
} from "../api/bridgeClient";
import "./BridgePanel.css";

function StatusDot({ state }) {
  return <span className={`bridge-dot bridge-dot-${state}`} aria-hidden="true" />;
}

function formatTime(ts) {
  if (!ts) return "—";
  const d = new Date(ts * 1000);
  return d.toLocaleTimeString("he-IL", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

export default function BridgePanel() {
  const [health, setHealth] = useState(null);
  const [manifest, setManifest] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    try {
      const [h, m] = await Promise.all([getBridgeHealth(), getBridgeManifest()]);
      setHealth(h);
      setManifest(m);
      setError(null);
    } catch (e) {
      setError(e.message);
      setHealth(null);
      setManifest(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 15000);
    return () => clearInterval(timer);
  }, []);

  const connected = Boolean(health?.ok);
  const serviceName = manifest?.name || health?.service || "IMA Local Bridge";
  const rootPath = manifest?.root || health?.root || "—";
  const capabilities = manifest?.capabilities || [];

  return (
    <div className="bridge-panel">
      {/* Connection status */}
      <div className={`bridge-status-card ${connected ? "connected" : "disconnected"}`}>
        <div className="bridge-status-header">
          <StatusDot state={connected ? "online" : "offline"} />
          <div>
            <strong>{serviceName}</strong>
            <span>{connected ? "מחובר" : loading ? "מתחבר…" : "מנותק"}</span>
          </div>
        </div>
        {error && <p className="bridge-error">{error}</p>}
      </div>

      {/* Sync path */}
      <div className="bridge-section">
        <span className="bridge-label">סנכרון נתונים</span>
        <div className="bridge-sync-path">
          <StatusDot state={connected ? "online" : "offline"} />
          <code>{rootPath}</code>
        </div>
        <p className="bridge-sync-note">
          נתיב השורש של Ima-kernel המקומי — מקור הנתונים לסנכרון.
        </p>
        {health?.timestamp && (
          <p className="bridge-timestamp">
            סנכרון אחרון: {formatTime(health.timestamp)}
          </p>
        )}
      </div>

      {/* Capabilities */}
      <div className="bridge-section">
        <span className="bridge-label">יכולות ה־Bridge</span>
        <div className="bridge-caps">
          {capabilities.length === 0 && !loading && (
            <p className="bridge-empty">אין יכולות זמינות</p>
          )}
          {capabilities.map((cap) => (
            <div key={cap} className="bridge-cap">
              <span className="bridge-cap-mark" />
              <div>
                <strong>{CAPABILITY_LABELS[cap] || cap}</strong>
                <span>{cap}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Raw manifest */}
      {manifest && (
        <details className="bridge-raw">
          <summary>מניפסט מלא</summary>
          <pre>{JSON.stringify(manifest, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}
