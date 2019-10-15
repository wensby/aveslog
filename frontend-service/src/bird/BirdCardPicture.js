import React from 'react';
import placeholder from './placeholder-bird.jpg';

export default ({ bird, ...other }) => {
  const style = { height: '150px', width: '150px', objectFit: 'cover' };
  const src = bird.thumbnailUrl || placeholder;
  return <img style={style} src={src} alt="Card" {...other} />;
};
