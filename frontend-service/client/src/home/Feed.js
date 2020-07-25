import React from 'react';
import { DateDelimiter } from './DateDelimiter';
import { SightingFeedItem } from './SightingFeedItem';

export const Feed = ({ items }) => {
  let date = null;
  const elements = [];

  items.forEach((item, index) => {
    const sightingDate = new Date(item.date);
    if (date === null || sightingDate < date) {
      elements.push(<DateDelimiter date={item.date} key={index + 'date'} />);
      date = sightingDate;
    }
    elements.push(
      <SightingFeedItem
        sighting={item}
        bird={item.bird}
        birder={item.birder}
      />
    );
  });

  return <div className='feed'>{elements}</div>;
};
