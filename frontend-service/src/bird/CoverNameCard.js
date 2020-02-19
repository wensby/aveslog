import React from 'react';
import { useCommonName } from './BirdHooks';
import './CoverNameCard.scss';

export function CoverNameCard({ bird }) {
  const { commonName, loading } = useCommonName(bird);

  return (
    <div className='bird-name-card'>
      <div>
        <h1 className='bird-page-name'>
          {loading ? '' : commonName || ''}</h1>
        <p>
          {bird.binomialName}
        </p>
      </div>
    </div>
  );
}
