import React from 'react';
import { BirdThumbnailImage } from './BirdThumbnailImage.js';
import { BirdLink } from './BirdLink.js';
import './CircledBirdPicture.scss';

export const CircledBirdPicture = ({ bird }) => {
  return (
    <div className='circled-bird-picture'>
      <BirdLink bird={bird} >
        <BirdThumbnailImage bird={bird} />
      </BirdLink>
    </div>
  );
};
