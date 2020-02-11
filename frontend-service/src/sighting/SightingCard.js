import React from 'react';
import { BirdCard } from '../bird/BirdCard.js';
import { BirdCardName } from '../bird/BirdCardName.js';
import { SightingTime } from './SightingTime.js';
import { useBird } from '../bird/BirdHooks.js';
import { CardBodyRight } from './CardBodyRight';
import './SightingCard.scss';

export function SightingCard({ sighting }) {
  const { bird } = useBird(sighting.birdId);

  if (!bird) {
    return <SightingCardPlaceholder />;
  }
  else {
    return (
      <BirdCard bird={bird}>
        <div className='sighting-card-body'>
          <div>
            <BirdCardName bird={bird} />
          </div>
          <CardBodyRight sighting={sighting} />
          <SightingTime className='card-text' sighting={sighting} />
        </div>
      </BirdCard>
    );
  }
}

export const SightingCardPlaceholder = React.forwardRef((props, ref) => {
  return <div ref={ref} className='sighting-card-body-placeholder' style={{ height: '152px' }} />;
});
