import React, { useContext } from 'react';
import { BirdCard } from './BirdCard';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { BirdCardName } from './BirdCardName';
import { useBird } from './BirdHooks';

export const BirdResultCard = ({ searchResult, ...other }) => {
  const { bird } = useBird(searchResult.id);
  const { t } = useTranslation();
  const { authenticated } = useContext(UserContext);

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
      <BirdCardName bird={bird} />
      {renderAddSightingLink(bird)}
    </BirdCard>
  );
};
