import { useState } from "react";
import { useI18n } from "../i18n/I18nProvider";
import { languages } from "../i18n/translations";
import IMAAvatar from "./IMAAvatar";
import AvatarPicker from "./AvatarPicker";
import GoogleLogin from "./GoogleLogin";
import "./Onboarding.css";

export default function Onboarding({ onComplete }) {
  const { t, lang, setLang } = useI18n();
  const [step, setStep] = useState(0);
  const [name, setName] = useState("");
  const [goals, setGoals] = useState([]);
  const [tone, setTone] = useState("warm");
  const [avatar, setAvatar] = useState("aura");
  const [googleData, setGoogleData] = useState(null);

  function handleGoogleLogin(data) {
    setGoogleData(data);
    if (data.name) setName(data.name);
    setStep(1);
  }

  function handleSkip() {
    onComplete({
      name: "",
      avatar: "aura",
      goals: [],
      preferences: { tone: "warm", responseLength: "medium" },
    });
  }

  function handleFinish() {
    onComplete({
      name: name.trim(),
      avatar,
      goals,
      preferences: { tone, responseLength: "medium" },
      google: googleData,
    });
  }

  const steps = [
    // 0: Welcome
    () => (
      <div className="onboard-step">
        <IMAAvatar variant="aura" size="lg" />
        <h1 className="onboard-title">{t("onboarding.welcome")}</h1>
        <p className="onboard-sub">{t("onboarding.welcomeSub")}</p>
        <button className="onboard-cta" onClick={() => setStep(1)}>
          {t("onboarding.next")}
        </button>
        <div className="onboard-divider">
          <span /> {t("common.comingSoon") === "בקרוב" ? "או" : "or"} <span />
        </div>
        <GoogleLogin
          onSuccess={handleGoogleLogin}
          label={t("google.continueWith")}
        />
        <button className="onboard-skip" onClick={handleSkip}>
          {t("onboarding.skip")}
        </button>
      </div>
    ),
    // 1: Language
    () => (
      <div className="onboard-step">
        <h2 className="onboard-heading">{t("onboarding.chooseLanguage")}</h2>
        <div className="onboard-lang-grid">
          {languages.map((l) => (
            <button
              key={l.code}
              className={`onboard-lang-card ${lang === l.code ? "onboard-lang-active" : ""}`}
              onClick={() => setLang(l.code)}
            >
              <span className="onboard-lang-label">{l.label}</span>
              <span className="onboard-lang-dir">{l.dir === "rtl" ? "RTL" : "LTR"}</span>
            </button>
          ))}
        </div>
        <div className="onboard-nav">
          <button className="onboard-back" onClick={() => setStep(0)}>
            {t("onboarding.back")}
          </button>
          <button className="onboard-cta" onClick={() => setStep(2)}>
            {t("onboarding.next")}
          </button>
        </div>
      </div>
    ),
    // 2: Avatar
    () => (
      <div className="onboard-step">
        <IMAAvatar variant={avatar} size="lg" />
        <h2 className="onboard-heading">{t("avatar.choose")}</h2>
        <AvatarPicker value={avatar} onChange={setAvatar} />
        <div className="onboard-nav">
          <button className="onboard-back" onClick={() => setStep(1)}>
            {t("onboarding.back")}
          </button>
          <button className="onboard-cta" onClick={() => setStep(3)}>
            {t("onboarding.next")}
          </button>
        </div>
      </div>
    ),
    // 3: Name
    () => (
      <div className="onboard-step">
        <h2 className="onboard-heading">{t("onboarding.yourName")}</h2>
        <input
          className="onboard-input"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder={t("onboarding.namePlaceholder")}
          autoFocus
          onKeyDown={(e) => e.key === "Enter" && setStep(4)}
        />
        <div className="onboard-nav">
          <button className="onboard-back" onClick={() => setStep(2)}>
            {t("onboarding.back")}
          </button>
          <button
            className="onboard-cta"
            onClick={() => setStep(4)}
            disabled={!name.trim()}
          >
            {t("onboarding.next")}
          </button>
        </div>
      </div>
    ),
    // 4: Goals
    () => (
      <div className="onboard-step">
        <h2 className="onboard-heading">{t("onboarding.whatToDo")}</h2>
        <div className="onboard-options">
          {t("onboarding.whatToDoOptions").map((opt, i) => (
            <button
              key={i}
              className={`onboard-chip ${goals.includes(i) ? "onboard-chip-active" : ""}`}
              onClick={() =>
                setGoals((prev) =>
                  prev.includes(i) ? prev.filter((g) => g !== i) : [...prev, i]
                )
              }
            >
              {opt}
            </button>
          ))}
        </div>
        <div className="onboard-nav">
          <button className="onboard-back" onClick={() => setStep(3)}>
            {t("onboarding.back")}
          </button>
          <button className="onboard-cta" onClick={() => setStep(5)}>
            {t("onboarding.next")}
          </button>
        </div>
      </div>
    ),
    // 5: Tone
    () => (
      <div className="onboard-step">
        <h2 className="onboard-heading">{t("onboarding.tone")}</h2>
        <div className="onboard-tone-list">
          {Object.entries(t("onboarding.toneOptions")).map(([key, label]) => (
            <button
              key={key}
              className={`onboard-tone-card ${tone === key ? "onboard-tone-active" : ""}`}
              onClick={() => setTone(key)}
            >
              <span className="onboard-tone-radio" />
              <span>{label}</span>
            </button>
          ))}
        </div>
        <div className="onboard-nav">
          <button className="onboard-back" onClick={() => setStep(4)}>
            {t("onboarding.back")}
          </button>
          <button className="onboard-cta" onClick={handleFinish}>
            {t("onboarding.finish")}
          </button>
        </div>
      </div>
    ),
  ];

  return (
    <div className="onboarding">
      <div className="onboard-progress">
        {steps.map((_, i) => (
          <span key={i} className={`onboard-dot ${i <= step ? "onboard-dot-active" : ""}`} />
        ))}
      </div>
      {steps[step]()}
    </div>
  );
}
