import React from 'react';
import { DateDelimiter } from './DateDelimiter';
import { SightingFeedItem } from './SightingFeedItem';

export const Feed = ({ sightings }) => {
  let date = null;
  const elements = [];

  sightings.forEach((sighting, index) => {
    const sightingDate = new Date(sighting.date);
    if (date === null || sightingDate < date) {
      elements.push(<DateDelimiter date={sighting.date} key={index + 'date'} />);
      date = sightingDate;
    }
    elements.push(
      <SightingFeedItem
        sighting={sighting}
        bird={sighting.bird}
        birder={sighting.birder}
      />
    );
  });

  return <div className='feed'>{elements}</div>;
};
