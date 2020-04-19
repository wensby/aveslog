import React from 'react';
import { withReveal } from 'generic/ScrollHooks.js';
import { useLazyBird } from 'bird/BirdHooks.js';
import { SightingListItemPlaceholder, SightingListItem } from './SightingListItem';

export const RevealableSightingListItem = withReveal(({ sighting, revealed }, ref) => {
  const bird = useLazyBird(sighting.birdId, revealed);
  if (!bird) return <SightingListItemPlaceholder ref={ref} />
  else return <SightingListItem ref={ref} sighting={sighting} bird={bird} />;
});
