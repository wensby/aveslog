import React from 'react';
import { withReveal } from '../generic/ScrollHooks.js';
import { useLazyBird } from './BirdHooks.js';
import { BirdSearchResultItem } from './BirdSearchResultItem.js';

export const RevealableBirdResultCard = withReveal(({ searchResult, revealed }, ref) => {
  const bird = useLazyBird(searchResult.id, revealed);
  return <BirdSearchResultItem bird={bird} ref={ref} stats={searchResult.stats} />
});
