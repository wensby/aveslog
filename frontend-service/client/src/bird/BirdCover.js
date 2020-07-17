import React from 'react';
import { CoverNameCard } from './CoverNameCard';
import './BirdCover.scss';

export function BirdCover({ bird }) {
  let style = {};
  if (bird.cover) {
    style = { backgroundImage: `url(${bird.cover.url})` };
  }
  return (
    <div className='picture-cover-container' style={style}>
      <div className='picture-cover'></div>
      <CoverNameCard bird={bird} />
    </div>
  );
}
