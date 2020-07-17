import React from 'react';

export function SightingTime({ sighting, ...props }) {
  if (sighting.time) {
    return <small {...props}>{`${sighting.date} ${sighting.time}`}</small>;
  }
  else {
    return <small {...props}>{sighting.date}</small>;
  }
};
