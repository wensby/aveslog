import React from 'react';
import { SightingFeedItemContainer } from './SightingFeedItemContainer';
import { DateDelimiter } from './DateDelimiter';

export const Feed = ({ sightings }) => {
  let date = null;
  const elements = [];

  sightings.forEach((sighting, index) => {
    const sightingDate = new Date(sighting.date);
    if (date === null || sightingDate < date) {
      elements.push(<DateDelimiter date={sighting.date} key={index + 'date'} />);
      date = sightingDate;
    }
    elements.push(<SightingFeedItemContainer sighting={sighting} key={index} />);
  });

  return <>{elements}</>;
};
