import { useState } from "react";
import { useI18n } from "../i18n/I18nProvider";
import { languages } from "../i18n/translations";
import DeveloperPanel from "./DeveloperPanel";
import "./SettingsView.css";

export default function SettingsView({ user, updateUser, resetUser }) {
  const { t, lang, setLang } = useI18n();
  const [section, setSection] = useState("main");

  function renderMain() {
    return (
      <div className="settings-list">
        {/* Profile */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.profile")}</span>
          <div className="settings-row">
            <span className="settings-row-label">{t("settings.name")}</span>
            <input
              className="settings-input"
              value={user.name}
              onChange={(e) => updateUser({ name: e.target.value })}
              placeholder={t("onboarding.namePlaceholder")}
            />
          </div>
        </div>

        {/* Language */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.language")}</span>
          <div className="settings-lang-options">
            {languages.map((l) => (
              <button
                key={l.code}
                className={`settings-lang-btn ${lang === l.code ? "settings-lang-active" : ""}`}
                onClick={() => setLang(l.code)}
              >
                {l.label}
              </button>
            ))}
          </div>
        </div>

        {/* Preferences */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.preferences")}</span>
          <div className="settings-row">
            <span className="settings-row-label">{t("settings.tone")}</span>
            <select
              className="settings-select"
              value={user.preferences.tone}
              onChange={(e) =>
                updateUser({
                  preferences: { ...user.preferences, tone: e.target.value },
                })
              }
            >
              {Object.entries(t("onboarding.toneOptions")).map(([key, label]) => (
                <option key={key} value={key}>
                  {label}
                </option>
              ))}
            </select>
          </div>
          <div className="settings-row">
            <span className="settings-row-label">{t("settings.responseLength")}</span>
            <select
              className="settings-select"
              value={user.preferences.responseLength}
              onChange={(e) =>
                updateUser({
                  preferences: {
                    ...user.preferences,
                    responseLength: e.target.value,
                  },
                })
              }
            >
              {Object.entries(t("settings.lengthOptions")).map(([key, label]) => (
                <option key={key} value={key}>
                  {label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Privacy */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.privacy")}</span>
          <div className="settings-info-card">
            <p className="settings-info-text">{t("privacy.storedLocally")}</p>
            <p className="settings-info-text">{t("privacy.noServices")}</p>
          </div>
          <button
            className="settings-danger-btn"
            onClick={() => {
              if (confirm(t("privacy.deleteConfirm"))) {
                resetUser();
              }
            }}
          >
            {t("privacy.deleteAll")}
          </button>
        </div>

        {/* Developer */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.developer")}</span>
          <button
            className="settings-nav-btn"
            onClick={() => setSection("developer")}
          >
            {t("developer.title")}
            <span className="settings-chevron" />
          </button>
        </div>

        {/* About */}
        <div className="settings-group">
          <span className="settings-group-label">{t("settings.about")}</span>
          <div className="settings-info-card">
            <p className="settings-info-text">IMA v2.2.1</p>
            <p className="settings-info-text">{t("brand.tagline")}</p>
          </div>
        </div>

        {/* Reset */}
        <button className="settings-reset-btn" onClick={resetUser}>
          {t("settings.logout")}
        </button>
      </div>
    );
  }

  return (
    <div className="settings-view">
      {section === "main" && renderMain()}
      {section === "developer" && (
        <DeveloperPanel onBack={() => setSection("main")} />
      )}
    </div>
  );
}
