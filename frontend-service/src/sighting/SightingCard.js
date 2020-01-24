import React from 'react';
import { BirdCard } from '../bird/BirdCard.js';
import { BirdCardName } from '../bird/BirdCardName.js';
import { SightingTime } from './SightingTime.js';
import { useBird } from '../bird/BirdHooks.js';
import { CardBodyRight } from './CardBodyRight';

export function SightingCard({ sighting }) {
  const { bird } = useBird(sighting.birdId);

  if (!bird) {
    return null;
  }
  else {
    return (
      <BirdCard bird={bird}>
        <div className='card-body'>
          <BirdCardName bird={bird} />
          <SightingTime className='card-text' sighting={sighting} />
        </div>
        <CardBodyRight sighting={sighting} />
      </BirdCard>
    );
  }
}
