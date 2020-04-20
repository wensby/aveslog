import React from 'react';
import { useBird } from './BirdHooks';
import { DetailedBirdCard } from './DetailedBirdCard';
import { Redirect } from 'react-router';

export const BirdPage = ({ match }) => {
  const { bird, error } = useBird(match.params.birdId);
  if (bird) return <DetailedBirdCard bird={bird} />;
  else if (error) return <Redirect to='/home' />;
  else return null;
};
