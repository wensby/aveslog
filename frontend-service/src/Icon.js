import React from 'react'
import icons from './icons.svg';

export default ({name}) => (
  <svg viewBox='0 0 7 8'>
    <use xlinkHref={`${icons}#${name}`} />
  </svg>
);
