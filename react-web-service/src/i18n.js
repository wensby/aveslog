import i18n from "i18next";
import Backend from 'i18next-xhr-backend';
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";
import i18next from "i18next";

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    ns: ['translation', 'bird'],
    defaultNS: 'translation',
    fallbackLng: 'en',
    keySeparator: false,
    debug: true,
    interpolation: {
      escapeValue: false
    }
  }, (err, t) => {
    i18next.t('myKey'); // key in translation namespace (defined default)
    i18next.t('bird:myKey') // key in bird namespace
  });

  export default i18n;
