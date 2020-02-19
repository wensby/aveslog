import React from 'react';
import { useTranslation } from "react-i18next";
import { PasswordChangeForm } from './PasswordChangeForm';

export default function Settings() {
  const { t } = useTranslation();
  return (<div>
    <h1>{t('Settings')}</h1>
    <h2>{t('change-password')}</h2>
    <PasswordChangeForm />
  </div>);
}
