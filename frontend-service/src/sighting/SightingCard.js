import React, { useContext } from 'react';
import { BirdCardName } from '../bird/BirdCardName.js';
import { SightingTime } from './SightingTime.js';
import { useBird } from '../bird/BirdHooks.js';
import { BirdThumbnailImage } from '../bird/BirdThumbnailImage.js';
import { BirdLink } from '../bird/BirdLink.js';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext.js';
import { Link } from 'react-router-dom';
import './SightingCard.scss';

export function SightingCard({ sighting }) {
  const { bird } = useBird(sighting.birdId);
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  if (!bird) {
    return <SightingCardPlaceholder />;
  }

  return (
    <div className='sighting-card' >
      <div className='picture'>
        <BirdLink bird={bird} >
          <BirdThumbnailImage bird={bird} />
        </BirdLink>
      </div>
      <div className='details'>
        <div className='name'>
          <BirdCardName bird={bird} className='common-name' />
          <div className='binomial-name'>{bird.binomialName}</div>
        </div>
        <SightingTime className='card-text' sighting={sighting} />
        {sighting.birderId === account.birder.id && <div className='card-body text-right'>
          <Link to={`/sighting/${sighting.id}`} className='card-link'>
            {t('sighting-item-edit-link')}
          </Link>
        </div>}
      </div>
    </div>
  );
}

export const SightingCardPlaceholder = React.forwardRef((props, ref) => {
  return <div ref={ref} className='sighting-card placeholder' />;
});
