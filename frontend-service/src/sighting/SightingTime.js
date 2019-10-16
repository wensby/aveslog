import React from 'react';

export default ({ sighting, ...props }) => {
  if (sighting.time) {
    return <p {...props}>{`${sighting.date} ${sighting.time}`}</p>;
  }
  else {
    return <p {...props}>{sighting.date}</p>;
  }
};
