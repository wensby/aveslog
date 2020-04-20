import React from 'react';
import { useBird, useCommonName } from './BirdHooks';
import { DetailedBirdCard } from './DetailedBirdCard';
import { Redirect } from 'react-router';
import { useTitle } from 'specific/TitleContext';

export const BirdPage = ({ match }) => {
  const { bird, error } = useBird(match.params.birdId);
  const { commonName } = useCommonName(bird);
  useTitle(commonName);
  if (bird) return <DetailedBirdCard bird={bird} />;
  else if (error) return <Redirect to='/home' />;
  else return null;
};
