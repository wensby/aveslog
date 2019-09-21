import React from 'react';
import { useTranslation } from "react-i18next";

export default function Settings() {
  const { t, i18n } = useTranslation();

  const changeLanguage = lng => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="container">
      <h1>{t('Settings')}</h1>
      <button className="nav-link" onClick={() => changeLanguage('en')}>English</button>
      <button className="nav-link" onClick={() => changeLanguage('sv')}>Svenska</button>
      <button className="nav-link" onClick={() => changeLanguage('kr')}>한국어</button>
    </div>
  );
}