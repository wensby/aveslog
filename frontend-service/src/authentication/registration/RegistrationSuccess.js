import React from 'react';
import { useTranslation } from 'react-i18next';

export function RegistrationSuccess() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('registration-success-title')}</h1>
      <p>{t('registration-success-message')}</p>
    </div>
  );
}
