import React from 'react';
import { Link } from 'react-router-dom';
import './BirderLink.scss';

export const BirderLink = ({ birder }) => {
  return (
    <div className='birder-link'>
      <Link to={`/birders/${birder.id}`}>{birder.name}</Link>
    </div>
  );
}
