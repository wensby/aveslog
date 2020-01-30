import React from 'react';
import { useBirdName } from './BirdHooks';

export function CoverNameCard({ bird }) {
  const { local, binomial, loading } = useBirdName(bird);

  return (
    <div className='w-100 d-flex justify-content-center'>
      <div className='shadow bg-white text-center pt-1 mb-0 px-2 rounded-top'>
        <h1 className='text-dark bird-page-name pb-2 mb-0'>
          {loading ? '' : local || ''}</h1>
        <p className='font-italic font-weight-light text-muted mb-0 pb-2'>
          {binomial}</p>
      </div>
    </div>
  );
}
