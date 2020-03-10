import React from 'react';
import { Link } from 'react-router-dom';

export const BirderLink = ({ birder }) => {
  return (
    <div>
      <Link to={`/birders/${birder.id}`}>{birder.name}</Link>
    </div>
  );
}
