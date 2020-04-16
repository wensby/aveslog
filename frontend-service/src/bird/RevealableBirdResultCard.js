import React from 'react';
import { withReveal } from '../generic/ScrollHooks.js';
import { useLazyBird } from './BirdHooks.js';
import { BirdSearchResultCard } from './BirdSearchResultCard.js';

export const RevealableBirdResultCard = withReveal(({ searchResult, revealed }, ref) => {
  const bird = useLazyBird(searchResult.id, revealed);
  return <BirdSearchResultCard bird={bird} ref={ref} stats={searchResult.stats} />
});
