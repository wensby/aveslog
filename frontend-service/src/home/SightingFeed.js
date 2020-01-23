import React from 'react';
import { SightingFeedItemContainer } from './SightingFeedItemContainer';
import { DateDelimiter } from './DateDelimiter';

export function SightingFeed({ sightings }) {
  let date = null;
  const elements = [];
  sightings.forEach(sighting => {
    const sightingDate = new Date(sighting.date);
    if (date === null || sightingDate < date) {
      elements.push(<DateDelimiter date={sighting.date} />);
      date = sightingDate;
    }
    elements.push(<SightingFeedItemContainer sighting={sighting} />);
  });
  return <>{elements}</>;
}
