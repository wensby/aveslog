import React from 'react';
import { useBird } from '../bird/BirdHooks';
import { useBirder } from '../birder/BirderHooks';
import { SightingFeedItem } from './SightingFeedItem';

export default function SightingFeed({ sightings }) {
  return <>{sightings.map(sighting => <SightingFeedItemContainer sighting={sighting} />)}</>;
}

function SightingFeedItemContainer({ sighting }) {
  const bird = useBird(sighting.birdId);
  const birder = useBirder(sighting.birderId);
  if (!bird || !birder) {
    return null;
  }
  return <SightingFeedItem sighting={sighting} bird={bird} birder={birder} />;
}
