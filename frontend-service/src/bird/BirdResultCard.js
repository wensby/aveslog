import React, { useState, useEffect, useContext } from 'react';
import BirdCard from './BirdCard';
import birdRepository from './BirdRepository';
import NewBirdSightingLink from './NewBirdSightingLink';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useTranslation } from 'react-i18next';
import BirdCardName from './BirdCardName';

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
      <div className="card-body">
        <BirdCardName bird={bird} />
        {renderAddSightingLink(bird)}
      </div>
    </BirdCard>
  );
}
