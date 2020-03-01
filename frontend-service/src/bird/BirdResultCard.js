import React, { useContext } from 'react';
import { BirdCard } from './BirdCard';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { BirdCardName } from './BirdCardName';
import { useLazyBird } from './BirdHooks';
import { useReveal } from '../generic/ScrollHooks';

export const BirdResultCard = ({ searchResult, ...other }) => {
  const ref = React.createRef();
  const revealed = useReveal(ref, 500);
  const bird = useLazyBird(searchResult.id, revealed);
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
    return <BirdResultCardPlaceholder ref={ref} />;
  }
  
  return (
    <BirdCard ref={ref} bird={bird} {...other} >
      <BirdCardName bird={bird} />
      {renderAddSightingLink(bird)}
    </BirdCard>
  );
};

export const BirdResultCardPlaceholder = React.forwardRef((props, ref) => {
  return <div ref={ref} className='sighting-card-body-placeholder' style={{ height: '150px' }} />;
});
