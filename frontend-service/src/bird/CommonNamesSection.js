import React, { useState, useEffect } from 'react';
import { CommonNameItem } from './CommonNameItem.js';
import './CommonNamesSection.scss';
import { useTranslation } from 'react-i18next';
import { CommonNameAdder } from './CommonNameAdder.js';
import { useLocales } from './LocalesHooks.js';
import { usePermissions } from '../account/AccountHooks.js'

export function CommonNamesSection({ bird }) {
  const { permissions } = usePermissions();
  const locales = useLocales();
  const [commonNames, setCommonNames] = useState([])
  const [namesByLanguageCode, setNamesByLanguageCode] = useState({});
  const [vacantLocales, setVacantLocales] = useState([]);

  useEffect(() => {
    const resolveCommonNames = async () => {
      const response = await fetch(`${window._env_.API_URL}/birds/${bird.id}/common-names`);
      if (response.status === 200) {
        const json = await response.json();
        setCommonNames(json.items);
      }
    };
    resolveCommonNames();
  }, []);

  const cacheBustAndRefetchCommonNames = () => {
    const resolveCommonNames = async () => {
      const response = await fetch(`${window._env_.API_URL}/birds/${bird.id}/common-names`, {
        cache: 'reload',
      });
      if (response.status === 200) {
        const json = await response.json();
        setCommonNames(json.items);
      }
    };
    resolveCommonNames();
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
  }, [namesByLanguageCode])

  const permissionToPostCommonNames = permissions
    .filter(x => x.method === 'POST')
    .filter(x => RegExp(x.resource_regex).test(`/birds/${bird.id}/common-names`)).length > 0;
  const { t } = useTranslation();

  return (
    <div className='common-names-section'>
      <h2>{t('common-names-title')}</h2>
      <div className='names-cluster'>
        {Object.entries(namesByLanguageCode).map(([key, value]) => <CommonNameItem key={key + value} code={key} name={value} />)}
      </div>
      {vacantLocales.length > 0 && permissionToPostCommonNames && <CommonNameAdder onNameAdded={cacheBustAndRefetchCommonNames} birdId={bird.id} locales={vacantLocales} />}
    </div>

  );
}
