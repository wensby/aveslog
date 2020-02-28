import React, { useState } from 'react';
import placeholder from './placeholder-bird.jpg';
import './BirdCardPicture.scss';

export const BirdCardPicture = ({ bird, ...other }) => {
  const [src, setSrc] = useState(((bird || {}).thumbnail || {}).url || placeholder);
  return <img
    className='bird-picture'
    onError={() => setSrc(placeholder)}
    src={src}
    alt="Card"
    {...other}
  />;
};
