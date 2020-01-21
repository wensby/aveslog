import React from 'react';
import { useBird } from './BirdHooks';
import { DetailedBirdCard } from './DetailedBirdCard';

export function BirdPage({ match }) {
  const { bird } = useBird(match.params.birdId);
  return bird ? <DetailedBirdCard bird={bird} /> : null;
}
