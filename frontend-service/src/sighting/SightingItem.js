import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';
import BirdCardPicture from '../bird/BirdCardPicture.js';

export default ({ sighting }) => {
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

  const renderPicture = () => {
    const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');
    return (
      <div className='col-sm-4' id='card-bird-thumbnail-col'>
        <Link to={`/bird/${formattedName}`}>
          <BirdCardPicture bird={bird} className={'card-bird-thumbnail'} />
        </Link>
      </div>
    );
  };

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
      {renderItemName()}
      <p className='card-text'>{getSightingTimeFormatted()}</p>
    </div>);
  };

  const renderItemName = () => {
    if (bird) {
      const localeName = t(`bird:${bird.binomialName}`, { fallbackLng: [] });
      if (localeName !== bird.binomialName) {
        return [
          <h5 key='1' className="card-title">{localeName}</h5>,
          <h6 key='2' className="card-subtitle mb-2 text-muted">
            {bird.binomialName}
          </h6>
        ];
      }
      else {
        return <h5 key='1' className="card-title">{bird.binomialName}</h5>;
      }
    }
    else {
      return <h5>...</h5>;
    }
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
      <div className='card'>
        <div className='row no-gutters'>
          {renderPicture()}
          {renderCardBody()}
          {renderCardBodyRight()}
        </div>
      </div>
    );
  }
}
