import React from 'react';
import { useBirdName } from './BirdHooks';

export function BirdCardName({ bird }) {
  const { local, binomial, loading } = useBirdName(bird);

  if (loading) {
    return null;
  }
  else if (local) {
    return (
      <>
        <h5 key='1' className="card-title">{local}</h5>
        <h6 key='2' className="card-subtitle mb-2 text-muted">
          {binomial}
        </h6>
      </>
    )
  }
  return <h5 key='1' className="card-title">{binomial}</h5>;
};
