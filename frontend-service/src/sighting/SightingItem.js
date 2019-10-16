import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';
import BirdCard from '../bird/BirdCard.js';
import BirdCardName from '../bird/BirdCardName.js';

export default ({ sighting, ...other }) => {
  const { account } = useContext(AuthenticationContext);
  const [bird, setBird] = useState(null);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();

  useEffect(() => {
    const resolveBird = async () => {
      const bird = await birdRepository.getBird(sighting.birdId);
      setBird(bird);
      setLoading(false);
    };
    resolveBird();
  }, [sighting]);

  const getSightingTimeFormatted = () => {
    if (sighting.time) {
      return `${sighting.date} ${sighting.time}`;
    }
    else {
      return sighting.date;
    }
  };

  const renderCardBody = () => {
    return (<div className='card-body'>
      <BirdCardName bird={bird} />
      <p className='card-text'>{getSightingTimeFormatted()}</p>
    </div>);
  };

  const renderCardBodyRight = () => {
    if (sighting.personId === account.personId) {
      return (<div className='card-body text-right'>
        <Link to={`/sighting/${sighting.sightingId}`} className='card-link'>
          {t('sighting-item-edit-link')}
        </Link>
      </div>);
    }
  };

  if (!account || loading) {
    return null;
  }
  else {
    return (
      <BirdCard bird={bird} {...other}>
        {renderCardBody()}
        {renderCardBodyRight()}
      </BirdCard>
    );
  }
}
