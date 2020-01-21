import React from 'react';
import { SightingFeedItemContainer } from './SightingFeedItemContainer';

export function SightingFeed({ sightings }) {
  return <>{sightings.map(sighting => <SightingFeedItemContainer sighting={sighting} />)}</>;
}
