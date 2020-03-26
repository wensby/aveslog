import React from 'react';
import { BirdThumbnailImage } from './BirdThumbnailImage.js';
import './CircledBirdPicture.scss';

export const CircledBirdPicture = ({ bird }) => {
  return (
    <div className='circled-bird-picture'>
      <BirdThumbnailImage bird={bird} />
    </div>
  );
};
