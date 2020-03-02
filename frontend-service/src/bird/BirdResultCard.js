import React, { useContext, forwardRef } from 'react';
import { BirdCard } from './BirdCard';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { BirdCardName } from './BirdCardName';
import { useLazyBird } from './BirdHooks';
import { withReveal } from '../generic/ScrollHooks';

export const RevealableBirdResultCard = withReveal(({ searchResult, revealed }, ref) => {
  const bird = useLazyBird(searchResult.id, revealed);
  return <BirdResultCard bird={bird} ref={ref}/>
});

const BirdResultCard = React.memo(forwardRef(({bird}, ref) => {
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
