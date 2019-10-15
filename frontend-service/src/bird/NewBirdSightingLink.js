import React from 'react';
import { Link } from 'react-router-dom';

export default ({ bird, children }) => {
  const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');
  const path = `/bird/${formattedName}/new-sighting`;
  return <Link to={path}>{children}</Link>;
}
