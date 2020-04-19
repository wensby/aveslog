import React, { memo, forwardRef, useContext } from 'react';
import { UserContext } from '../authentication/UserContext.js';
import { useTranslation } from 'react-i18next';
import { PictureBirdLink } from '../bird/PictureBirdLink.js';
import { BirdCardName } from '../bird/BirdCardName.js';
import { SightingTime } from './SightingTime.js';
import { Link } from 'react-router-dom';
import './SightingListItem.scss';

export const SightingListItem = memo(forwardRef(({ sighting, bird }, ref) => {
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  return (
    <div className='sighting-list-item' ref={ref}>
      <PictureBirdLink bird={bird} />
      <div className='details'>
        <div className='name'>
          <BirdCardName bird={bird} className='common-name' />
          <div className='binomial-name'>{bird.binomialName}</div>
        </div>
        <SightingTime sighting={sighting} />
        {sighting.birderId === account.birder.id && <div>
          <Link to={`/sighting/${sighting.id}`}>
            {t('sighting-item-edit-link')}
          </Link>
        </div>}
      </div>
    </div>
  );
}));

export const SightingListItemPlaceholder = memo(forwardRef((props, ref) => {
  return <div ref={ref} className='sighting-list-item' />;
}));
