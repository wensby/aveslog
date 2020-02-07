import React from 'react';
import { SightingCard, SightingCardPlaceholder } from './SightingCard.js';
import { LazyLoad } from '../LazyLoad.js';

export const SightingList = ({ sightings }) => {

  const renderSightingCard = sighting => {
    return (
      <LazyLoad offset={1000} key={sighting.id} placeholder={<SightingCardPlaceholder />}>
        <SightingCard sighting={sighting} />
      </LazyLoad>
    );
  };

  return <div className='text-break'>{sightings.map(renderSightingCard)}</div>;
};
