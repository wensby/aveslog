import React from 'react';
import { useBirdPicture } from './BirdHooks';
import './BirdThumbnailImage.scss';

export const BirdThumbnailImage = ({ bird, ...other }) => {
  const src = useBirdPicture(bird);

  return <img
    className='bird-thumbnail'
    src={src}
    alt="Card"
    {...other}
  />;
};
