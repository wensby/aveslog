import React from 'react';
import { BirdCardPicture } from './BirdCardPicture';
import BirdLink from './BirdLink';
import './BirdCard.scss';

export function BirdCard({ bird, children }) {
  return (
    <div className='bird-card'>
      <div className='bird-card-picture img-square-wrapper'>
        <BirdLink bird={bird} >
          <BirdCardPicture bird={bird} />
        </BirdLink>
      </div>
      <div className='bird-card-body'>
        {children}
      </div>
    </div>
  );
};
