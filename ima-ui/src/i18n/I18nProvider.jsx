import { createContext, useContext, useState, useEffect, useCallback } from "react";
import translations, { languages } from "./translations";

const I18nContext = createContext(null);

function getNested(obj, path) {
  return path.split(".").reduce((acc, key) => acc?.[key], obj);
}

export function I18nProvider({ children }) {
  const [lang, setLangState] = useState(() => {
    return localStorage.getItem("ima-lang") || "he";
  });

  const dir = translations[lang].dir;

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = dir;
    localStorage.setItem("ima-lang", lang);
  }, [lang, dir]);

  const setLang = useCallback((code) => {
    if (translations[code]) setLangState(code);
  }, []);

  const t = useCallback(
    (key) => {
      const val = getNested(translations[lang], key);
      return val !== undefined ? val : key;
    },
    [lang]
  );

  return (
    <I18nContext.Provider value={{ lang, setLang, dir, t, languages }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useI18n must be used within I18nProvider");
  return ctx;
}
