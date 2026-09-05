import { useState } from "react";
import { useI18n } from "../i18n/I18nProvider";
import IMAAvatar from "./IMAAvatar";
import "./Landing.css";

export default function Landing({ onStartChat, avatar = "aura" }) {
  const { t } = useI18n();
  const [input, setInput] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;
    onStartChat(input.trim());
  }

  const features = [
    { key: "chat", icon: "💬" },
    { key: "memory", icon: "🧠" },
    { key: "learning", icon: "📚" },
    { key: "voice", icon: "🎙" },
    { key: "multilingual", icon: "🌍" },
    { key: "actions", icon: "⚡" },
  ];

  return (
    <div className="landing">
      <div className="landing-hero">
        <IMAAvatar variant={avatar} size="lg" />
        <h1 className="landing-brand">{t("brand.name")}</h1>
        <p className="landing-tagline">{t("brand.tagline")}</p>
        <p className="landing-subtitle">{t("brand.subtitle")}</p>
      </div>

      <form className="landing-chat-form" onSubmit={handleSubmit}>
        <input
          className="landing-chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t("landing.chatPlaceholder")}
          autoFocus
        />
        <button type="submit" className="landing-chat-btn" disabled={!input.trim()}>
          <span className="landing-send-icon" />
        </button>
      </form>

      <div className="landing-features">
        {features.map((f) => (
          <div key={f.key} className="landing-feature">
            <span className="landing-feature-icon">{f.icon}</span>
            <span className="landing-feature-label">
              {t(`landing.features.${f.key}`)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
