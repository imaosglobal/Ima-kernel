import i18next from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
i18next.use(LanguageDetector).init({
  fallbackLng:'en',
  resources:{ en:{translation:{}}, he:{translation:{}}, fr:{translation:{}} },
});
export default i18next;
