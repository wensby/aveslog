import React from 'react';
import { useBird } from './BirdHooks';
import { DetailedBirdCard } from './DetailedBirdCard';
import { Redirect } from 'react-router';

export function BirdPage({ match }) {
  const { bird, error } = useBird(match.params.birdId);
  return bird ? <DetailedBirdCard bird={bird} /> : (error !== null ? <Redirect to='/home' /> : null);
}
