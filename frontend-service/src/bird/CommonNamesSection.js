import React from 'react';
import { CommonNameItem } from './CommonNameItem.js';
import './CommonNamesSection.scss';
import { useTranslation } from 'react-i18next';
import { CommonNameAdder } from './CommonNameAdder.js';
import { useLocales } from './LocalesHooks.js';

export function CommonNamesSection({ bird }) {
  const locales = useLocales();
  const commonNames = bird.commonNames;
  const namesByLanguageCode = commonNames.reduce((map, obj) => {
    map[obj.locale] = obj.name;
    return map;
  }, {});
  const vacantLocales = locales.filter(x => !(x in namesByLanguageCode));
  const { t } = useTranslation();

  return (
    <div className='common-names-section'>
      <h2>{t('common-names-title')}</h2>
      <div className='names-cluster'>
        {Object.entries(namesByLanguageCode).map(([key, value]) => <CommonNameItem key={key+value} code={key} name={value} />)}
      </div>
      {vacantLocales.length > 0 && <CommonNameAdder birdId={bird.id} locales={vacantLocales} />}
    </div>

  );
}
