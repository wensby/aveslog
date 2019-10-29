import React from 'react';
import placeholder from './placeholder-bird.jpg';

export default function BirdCardPicture({ bird, ...other }) {
  const src = (bird && bird.thumbnailUrl) || placeholder;
  return <img className='bird-picture' src={src} alt="Card" {...other} />;
};
