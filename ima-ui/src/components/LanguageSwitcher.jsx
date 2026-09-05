import { useState, useRef, useEffect } from "react";
import { useI18n } from "../i18n/I18nProvider";
import "./LanguageSwitcher.css";

export default function LanguageSwitcher() {
  const { lang, setLang, languages, t } = useI18n();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const current = languages.find((l) => l.code === lang);

  return (
    <div className="lang-switcher" ref={ref}>
      <button
        className="lang-trigger"
        onClick={() => setOpen((v) => !v)}
        aria-label={t("settings.language")}
      >
        <span className="lang-globe" />
        <span className="lang-current">{current?.label || lang}</span>
      </button>
      {open && (
        <div className="lang-menu">
          {languages.map((l) => (
            <button
              key={l.code}
              className={`lang-option ${l.code === lang ? "lang-active" : ""}`}
              onClick={() => {
                setLang(l.code);
                setOpen(false);
              }}
            >
              {l.label}
              {l.code === lang && <span className="lang-check" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
