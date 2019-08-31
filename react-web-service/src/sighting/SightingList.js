import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository.js';
import SightingService from './SightingService.js';

function SightingItem(props) {
  const { sighting } = props;
  const [bird, setBird] = useState(null);
  const { t } = useTranslation();

  useEffect(() => {
    resolveBird();
  }, []);

  const resolveBird = async () => {
    const bird = await birdRepository.getBird(sighting.birdId);
    setBird(bird);
  };

  const getThumbnailUrl = () => {
    if (bird && bird.thumbnailUrl) {
      return bird.thumbnailUrl;
    }
  };

  const renderBirdThumbnail = () => {
    const url = getThumbnailUrl() || '/placeholder-bird.png';
    return <img src={url} className='img-fluid card-bird-thumbnail' />;
  };

  const renderPicture = () => {
    if (bird) {
      const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');
      return (
        <div className='col-sm-4' id='card-bird-thumbnail-col'>
          <Link to={`/bird/${formattedName}`}>{renderBirdThumbnail()}</Link>
        </div>
      );
    }
    else {
      return (
        <div className='col-sm-4' id='card-bird-thumbnail-col'>
          {renderBirdThumbnail()}
        </div>
      );
    }
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
    return (
      <div className='card-body'>
        {renderItemName()}
        <p className='card-text'>{getSightingTimeFormatted()}</p>
      </div>
    );
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
    return (
      <div className='card-body text-right'>
        <Link to={`/sighting/${sighting.sightingId}`} className='card-link'>
          {t('sighting-item-edit-link')}
        </Link>
      </div>
    );
  };

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

export default function SightingList({ }) {
  const [sightings, setSightings] = useState([]);
  const sightingService = new SightingService();

  const fetchSightings = async () => {
    const authToken = localStorage.getItem('authToken');
    const username = localStorage.getItem('username');
    const response = await sightingService.fetchSightings(username, authToken);
    if (response.status == 'success') {
      setSightings(response.result.sightings);
    }
  }

  useEffect(() => {
    fetchSightings();
  }, []);

  const renderSightingItem = sighting => {
    return <SightingItem sighting={sighting} key={sighting.sightingId} />;
  };

  return (
    <div className="text-break">
      {sightings.map(renderSightingItem)}
    </div>
  );
}
