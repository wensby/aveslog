import React from 'react';
import { useTranslation } from "react-i18next";

export default function Settings() {
  const { t } = useTranslation();

  return (
    <div className="container">
      <h1>{t('Settings')}</h1>
    </div>
  );
}
