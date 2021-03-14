import React from 'react';
import './CoverNameCard.scss';

export function CoverNameCard({ binomial, common }) {
  return (
    <div className='bird-name-card'>
      <h1 className='bird-page-name'>{common}</h1>
      <p className='binomial'>{binomial}</p>
    </div>
  );
}
