import React from 'react';
import { Link } from 'react-router-dom';

export const BirdLink = ({ bird, children }) => {
  const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');
  return <Link to={`/bird/${formattedName}`}>{children}</Link>
};
