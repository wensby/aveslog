import React from 'react';
import { useCommonName } from './BirdHooks';
import { FadeInBottom } from './FadeInBottom';
import './BirdCardName.scss';

export function BirdCardName({ bird }) {
  const { commonName, loading } = useCommonName(bird);

  if (loading) {
    return null;
  }
  else if (commonName) {
    return (
      <>
        <FadeInBottom>
          <h5 key='1' className="card-title">{commonName}</h5>
        </FadeInBottom>
        <h6 key='2' className="card-subtitle mb-2 text-muted">
          {bird.binomialName}
        </h6>
      </>
    )
  }
  return <h5 key='1' className="card-title">{bird.binomialName}</h5>;
};
