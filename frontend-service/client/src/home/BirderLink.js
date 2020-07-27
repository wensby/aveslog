import React from 'react';
import { Link } from 'react-router-dom';
import './BirderLink.scss';

export const BirderLink = ({ birder }) => {
  return (
    <Link to={`/birders/${birder.id}`}>
      <div className='birder-link'>
        {birder.name}
      </div>
    </Link>
  );
}
