import React from 'react';
import './CoverNameCard.scss';

export function CoverNameCard({ binomial, common }) {
  return (
    <div className='bird-name-card'>
      <div>
        <h1 className='bird-page-name'>{common}</h1>
        <p>{binomial}</p>
      </div>
    </div>
  );
}
