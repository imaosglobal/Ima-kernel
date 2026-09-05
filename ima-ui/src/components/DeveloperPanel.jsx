import { useState } from "react";
import { useI18n } from "../i18n/I18nProvider";
import BridgePanel from "./BridgePanel";
import { getHealth, getReady } from "../api/imaClient";
import { useEffect } from "react";
import "./DeveloperPanel.css";

export default function DeveloperPanel({ onBack }) {
  const { t } = useI18n();
  const [unlocked, setUnlocked] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);

  const [apiHealth, setApiHealth] = useState(null);
  const [apiReady, setApiReady] = useState(null);

  useEffect(() => {
    if (!unlocked) return;
    let alive = true;
    async function check() {
      try {
        const [h, r] = await Promise.all([getHealth(), getReady()]);
        if (alive) {
          setApiHealth(h);
          setApiReady(r);
        }
      } catch {
        if (alive) {
          setApiHealth(null);
          setApiReady(null);
        }
      }
    }
    check();
    const timer = setInterval(check, 15000);
    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, [unlocked]);

  function handleEnter() {
    // Simple gate — not real security, just a UX barrier
    if (password === "ima-dev" || password === "developer") {
      setUnlocked(true);
      setError(false);
    } else {
      setError(true);
    }
  }

  if (!unlocked) {
    return (
      <div className="dev-panel">
        <button className="dev-back-btn" onClick={onBack}>
          {t("common.back")}
        </button>
        <div className="dev-gate">
          <div className="dev-gate-icon" />
          <h2 className="dev-gate-title">{t("developer.enter")}</h2>
          <p className="dev-warning">{t("developer.warning")}</p>
          <input
            className="dev-password-input"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setError(false);
            }}
            placeholder={t("developer.passwordPlaceholder")}
            onKeyDown={(e) => e.key === "Enter" && handleEnter()}
            autoFocus
          />
          {error && <p className="dev-error">{t("developer.wrongPassword")}</p>}
          <button className="dev-enter-btn" onClick={handleEnter}>
            {t("common.confirm")}
          </button>
          <p className="dev-hint">ima-dev</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dev-panel">
      <button className="dev-back-btn" onClick={onBack}>
        {t("common.back")}
      </button>

      <div className="dev-section">
        <span className="dev-section-label">{t("developer.systemHealth")}</span>
        <div className="dev-health-grid">
          <div className="dev-health-card">
            <span className="dev-health-name">/health</span>
            <span className={`dev-health-status ${apiHealth ? "ok" : "down"}`}>
              {apiHealth ? "OK" : "DOWN"}
            </span>
          </div>
          <div className="dev-health-card">
            <span className="dev-health-name">/ready</span>
            <span className={`dev-health-status ${apiReady ? "ok" : "down"}`}>
              {apiReady ? "OK" : "DOWN"}
            </span>
          </div>
        </div>
      </div>

      <div className="dev-section">
        <span className="dev-section-label">{t("developer.bridge")}</span>
        <BridgePanel />
      </div>
    </div>
  );
}
