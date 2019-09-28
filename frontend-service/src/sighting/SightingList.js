import React from 'react';
import SightingItem from './SightingItem.js';

export default ({ sightings }) => {

  const renderSightingItem = sighting => {
    return <SightingItem sighting={sighting} key={sighting.sightingId} />;
  };

  return <div className='text-break'>{sightings.map(renderSightingItem)}</div>;
}
