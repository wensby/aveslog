import React, { useState, useEffect } from 'react';
import { CommonNameItem } from './CommonNameItem.js';
import './CommonNamesSection.scss';
import { useTranslation } from 'react-i18next';
import { CommonNameAdder } from './CommonNameAdder.js';
import { useLocales } from './LocalesHooks.js';
import { useResourcePermission } from '../account/AccountHooks.js'
import { useCommonNames } from '../bird/BirdHooks.js';

export function CommonNamesSection({ bird }) {
  const [forceReloadNames, setForceReloadNames] = useState(false);
  const [namesByLanguageCode, setNamesByLanguageCode] = useState({});
  const [vacantLocales, setVacantLocales] = useState([]);
  const [showAdder, setShowAdder] = useState(false);
  const locales = useLocales();
  const commonNames = useCommonNames(bird, forceReloadNames);
  const permissionToPostCommonNames = useResourcePermission(`/birds/${bird.id}/common-names`, 'POST');
  const { t } = useTranslation();

  const cacheBustAndRefetchCommonNames = () => {
    setForceReloadNames(true);
    setInterval(() => { setForceReloadNames(false) }, 0);
  };

  useEffect(() => {
    if (commonNames.length > 0) {
      setNamesByLanguageCode(
        commonNames.reduce((map, obj) => {
          map[obj.locale] = obj.name;
          return map;
        }, {})
      )
    }
    else {
      setNamesByLanguageCode({});
    }
  }, [commonNames]);

  useEffect(() => {
    setVacantLocales(locales.filter(x => !(x in namesByLanguageCode)));
  }, [namesByLanguageCode, locales])

  useEffect(() => {
    setShowAdder(vacantLocales.length > 0 && permissionToPostCommonNames);
  }, [vacantLocales, permissionToPostCommonNames])

  return (
    <div className='common-names-section'>
      <h2>{t('common-names-title')}</h2>
      <div className='names-cluster'>
        {Object.entries(namesByLanguageCode).map(([key, value]) => <CommonNameItem key={key + value} code={key} name={value} />)}
      </div>
      {showAdder && <CommonNameAdder onNameAdded={cacheBustAndRefetchCommonNames} bird={bird} locales={vacantLocales} />}
    </div>

  );
}
