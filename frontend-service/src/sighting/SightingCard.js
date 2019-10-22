import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext.js';
import BirdCard from '../bird/BirdCard.js';
import BirdCardName from '../bird/BirdCardName.js';
import SightingTime from './SightingTime.js';
import { useBird } from '../bird/BirdHooks.js';

export default ({ sighting, ...other }) => {
  const bird = useBird(sighting.birdId);
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  const renderCardBodyRight = () => {
    if (sighting.personId === account.personId) {
      return (<div className='card-body text-right'>
        <Link to={`/sighting/${sighting.sightingId}`} className='card-link'>
          {t('sighting-item-edit-link')}
        </Link>
      </div>);
    }
  };

  if (!account || !bird) {
    return null;
  }
  else {
    return (
      <BirdCard bird={bird} {...other}>
        <div className='card-body'>
          <BirdCardName bird={bird} />
          <SightingTime sighting={sighting} className='card-text'/>
        </div>
        {renderCardBodyRight()}
      </BirdCard>
    );
  }
}
