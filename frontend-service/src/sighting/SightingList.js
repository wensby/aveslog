import React from 'react';
import { SightingCard } from './SightingCard.js';
import { LazyLoadComponent } from 'react-lazy-load-image-component';

export function SightingList({ sightings }) {

  const renderSightingCard = sighting => {
    return (
      <LazyLoadComponent placeholder={<div style={{height: '150px'}}></div>}><React.Fragment key={sighting.id}>
        <SightingCard sighting={sighting} key={sighting.id} />
      </React.Fragment></LazyLoadComponent>
    );
  };

  return <div className='text-break'>{sightings.map(renderSightingCard)}</div>;
}
