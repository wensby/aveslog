import React from 'react'
import icons from './icons.svg';

export default ({name, ...props}) => (
  <svg viewBox='0 0 7 8' {...props}>
    <use xlinkHref={`${icons}#${name}`} />
  </svg>
);
