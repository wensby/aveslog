import React from 'react';
import SightingCard from './SightingCard.js';

export default ({ sightings }) => {

  const renderSightingCard = sighting => {
    return (
      <React.Fragment key={sighting.id}>
        <SightingCard sighting={sighting} key={sighting.id} />
      </React.Fragment>
    );
  };

  return <div className='text-break'>{sightings.map(renderSightingCard)}</div>;
}
