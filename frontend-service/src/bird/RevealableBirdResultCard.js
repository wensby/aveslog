import React from 'react';
import { withReveal } from '../generic/ScrollHooks.js';
import { useLazyBird } from './BirdHooks.js';
import { BirdResultCard } from './BirdResultCard.js';

export const RevealableBirdResultCard = withReveal(({ searchResult, revealed }, ref) => {
  const bird = useLazyBird(searchResult.id, revealed);
  return <BirdResultCard bird={bird} ref={ref} />
});
