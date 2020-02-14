import React from 'react';
import { useCommonName } from '../bird/BirdHooks';

export function BirdSection({ bird }) {
  const { commonName, loading } = useCommonName(bird);

  return (
    <p>{loading ? '' : commonName || bird.binomialName}</p>
  );
}
