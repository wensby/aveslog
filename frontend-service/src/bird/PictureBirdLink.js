import React from 'react';
import { BirdLink } from './BirdLink.js';
import { CircledBirdPicture } from './CircledBirdPicture.js';

export const PictureBirdLink = ({ bird }) => {
  return (
    <BirdLink bird={bird} >
      <CircledBirdPicture bird={bird} />
    </BirdLink>
  );
};
