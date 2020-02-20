import React from 'react';
import { useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';
import { CommonNamesSection } from './CommonNamesSection';
import { BirdActionBar } from './BirdActionBar';
import './DetailedBirdCard.scss';

export function DetailedBirdCard({ bird }) {
  const stats = useBirdStatistics(bird);

  return (
    <div className='detailed-bird-card'>
      <BirdCover bird={bird} />
      <BirdActionBar bird={bird} />
      <CommonNamesSection bird={bird} />
      <hr />
      <div>
        Sightings: {stats.sightingsCount}
        <br />
        Lucky birders: {stats.birdersCount}
      </div>
      {bird.thumbnail &&
        <div>
          <p><small>{`Thumbnail Photo by: ${bird.thumbnail.credit}`}</small></p>
        </div>}
    </div>
  );
}
