import React from 'react';
import placeholder from './placeholder-bird.jpg';

export default ({ bird, ...other }) => {
  const style = { maxHeight: '150px' };
  const src = bird.thumbnailUrl || placeholder;
  return <img style={style} src={src} alt="Card" {...other} />;
};
