import React from 'react';
import placeholder from './placeholder-bird.jpg';

export default ({ bird }) => {
  const style = { maxHeight: '150px' };
  const src = bird.thumbnail || placeholder;
  return <img style={style} src={src} alt="Card" />;
};
