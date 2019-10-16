import React from 'react';
import SightingCard from './SightingCard.js';

export default ({ sightings }) => {

  const renderSightingCard = sighting => {
    return <SightingCard sighting={sighting} key={sighting.sightingId} />;
  };

  return <div className='text-break'>{sightings.map(renderSightingCard)}</div>;
}
