import React from 'react';
import { CommonNameItem } from './CommonNameItem';
import './CommonNamesSection.scss';
import { useTranslation } from 'react-i18next';

export function CommonNamesSection({ namesByLanguageCode }) {
  const { t } = useTranslation();
  return (
    <div className='common-names-section'>
      <h2>{t('common-names-title')}</h2>
      <div>
        {Object.entries(namesByLanguageCode).map(([key, value]) => <CommonNameItem code={key} name={value} />)}
      </div>
    </div>

  );
}
