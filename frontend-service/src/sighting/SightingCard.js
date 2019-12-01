import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext.js';
import BirdCard from '../bird/BirdCard.js';
import BirdCardName from '../bird/BirdCardName.js';
import SightingTime from './SightingTime.js';
import { useBird } from '../bird/BirdHooks.js';

export default function SightingCard({ sighting }) {
  const bird = useBird(sighting.birdId);

  if (!bird) {
    return null;
  }
  else {
    return (
      <BirdCard bird={bird}>
        <div className='card-body'>
          <BirdCardName bird={bird} />
          <SightingTime className='card-text' sighting={sighting} />
        </div>
        <CardBodyRight sighting={sighting} />
      </BirdCard>
    );
  }
}

function CardBodyRight({ sighting }) {
  const { account } = useContext(UserContext);
  const { t } = useTranslation();
  if (sighting.birderId !== account.birder.id) {
    return null;
  }
  return (
    <div className='card-body text-right'>
      <Link to={`/sighting/${sighting.id}`} className='card-link'>
        {t('sighting-item-edit-link')}
      </Link>
    </div>
  );
}
