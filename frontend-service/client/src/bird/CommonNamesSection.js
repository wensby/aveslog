import React, { useState, useEffect } from 'react';
import { CommonNameItem } from './CommonNameItem.js';
import { useTranslation } from 'react-i18next';
import { CommonNameAdder } from './CommonNameAdder.js';
import { useLocales } from './LocalesHooks.js';
import { useResourcePermission } from '../account/AccountHooks.js'
import './CommonNamesSection.scss';
import { CollapsableSection } from 'generic/CollapsableSection.js';
import { CollapsableSectionHeader } from 'generic/CollapsableSectionHeader.js';
import { CollapsableSectionBody } from 'generic/CollapsableSectionBody.js';

export function CommonNamesSection({ bird, commonNames }) {
  const [names, setNames] = useState(commonNames);
  const [namesByLanguageCode, setNamesByLanguageCode] = useState({});
  const [vacantLocales, setVacantLocales] = useState([]);
  const [showAdder, setShowAdder] = useState(false);
  const locales = useLocales();
  const permissionToPostCommonNames = useResourcePermission(`/birds/${bird.id}/common-names`, 'POST');
  const { t } = useTranslation();

  useEffect(() => {
    if (names.length > 0) {
      setNamesByLanguageCode(
        names.reduce((map, obj) => {
          map[obj.locale] = obj.name;
          return map;
        }, {})
      )
    }
    else {
      setNamesByLanguageCode({});
    }
  }, [names]);

  useEffect(() => {
    setVacantLocales(locales.filter(x => !(x in namesByLanguageCode)));
  }, [namesByLanguageCode, locales])

  useEffect(() => {
    setShowAdder(vacantLocales.length > 0 && permissionToPostCommonNames);
  }, [vacantLocales, permissionToPostCommonNames])

  return (
    <CollapsableSection>
      <CollapsableSectionHeader>
        <h2>{t('common-names-title')}</h2>
      </CollapsableSectionHeader>
      <CollapsableSectionBody>
        <div className='common-names-section'>
          <div className='names-cluster'>
            {Object.entries(namesByLanguageCode).map(([key, value]) => <CommonNameItem key={key + value} code={key} name={value} />)}
          </div>
          {showAdder && <CommonNameAdder onNameAdded={(language, name) => { setNames([...names, { locale: language, name: name }]) }} bird={bird} locales={vacantLocales} />}
        </div>
      </CollapsableSectionBody>
    </CollapsableSection>
  );
}
