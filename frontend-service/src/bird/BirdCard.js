import React from 'react';
import { BirdThumbnailImage } from './BirdThumbnailImage.js';
import BirdLink from './BirdLink';
import './BirdCard.scss';

export const BirdCard = ({ bird, children }) => {
  return (
    <div className='bird-card'>
      <div className='bird-card-picture'>
        <BirdLink bird={bird} >
          <BirdThumbnailImage bird={bird} />
        </BirdLink>
      </div>
      <div className='bird-card-body'>
        {children}
      </div>
    </div>
  );
};
