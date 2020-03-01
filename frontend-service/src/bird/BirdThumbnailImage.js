import React, { useState, useEffect } from 'react';
import placeholder from './placeholder-bird.jpg';
import './BirdThumbnailImage.scss';

export const BirdThumbnailImage = ({ bird, ...other }) => {
  const [src, setSrc] = useState(placeholder);

  useEffect(() => {
    if (((bird || {}).thumbnail || {}).url) {
      if (bird.thumbnail.url !== src) {
        setSrc(bird.thumbnail.url);
      }
    }
    else {
      setSrc(placeholder);
    }
  }, [bird, src])

  return <img
    className='bird-thumbnail'
    onError={() => setSrc(placeholder)}
    src={src}
    alt="Card"
    {...other}
  />;
};
