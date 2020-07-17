import React from 'react';
import { useTranslation } from "react-i18next";
import { PasswordChangeForm } from './PasswordChangeForm';
import { PageHeading } from 'generic/PageHeading';
import './Settings.scss';
import { BirderSettings } from './BirderSettings';

export const Settings = () => {
  const { t } = useTranslation();
  return (
    <div className='settings'>
      <PageHeading>{t('Settings')}</PageHeading>
      <BirderSettings />
      <h2>{t('change-password')}</h2>
      <PasswordChangeForm />
    </div>
  );
}
