import React, { useContext, forwardRef, memo } from 'react';
import { BirdCard } from './BirdCard';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { BirdCardName } from './BirdCardName';

export const BirdSearchResultCard = memo(forwardRef(({ bird }, ref) => {
  const { t } = useTranslation();
  const { authenticated } = useContext(UserContext);

  if (!bird) {
    return <div ref={ref} className='sighting-card-body-placeholder' style={{ height: '150px' }} />;
  }

  return (
    <BirdCard ref={ref} bird={bird} >
      <BirdCardName bird={bird} />
      {authenticated && <NewBirdSightingLink bird={bird}>{t('add-sighting-link')}</NewBirdSightingLink>}
    </BirdCard>
  );
}));
