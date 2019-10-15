import React, { useState, useEffect, useContext } from 'react';
import BirdCard from './BirdCard';
import birdRepository from './BirdRepository';
import NewBirdSightingLink from './NewBirdSightingLink';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useTranslation } from 'react-i18next';

export default ({ searchResult, ...other }) => {
  const [bird, setBird] = useState(null);
  const { t } = useTranslation();
  const { authenticated } = useContext(AuthenticationContext);

  const resultBird = async birdId => {
    setBird(await birdRepository.getBird(birdId));
  }

  useEffect(() => {
    resultBird(searchResult.birdId);
  }, [searchResult]);

  const renderItemName = item => {
    const localeName = t(`bird:${item.binomialName}`, {fallbackLng: []});
    if (localeName !== item.binomialName) {
      return [
        <h5 key='1' className="card-title">{localeName}</h5>,
        <h6 key='2' className="card-subtitle mb-2 text-muted">
          {item.binomialName}
        </h6>
      ];
    }
    else {
      return <h5 key='1' className="card-title">{item.binomialName}</h5>;
    }
  };

  const renderAddSightingLink = item => {
    if (authenticated) {
      return <NewBirdSightingLink bird={item}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
    else {
      return null;
    }
  };

  if (!bird) {
    return null;
  }
  
  return (
    <BirdCard bird={bird} {...other} >
      {renderItemName(bird)}
      {renderAddSightingLink(bird)}
    </BirdCard>
  );
}
