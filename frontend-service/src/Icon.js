import React from 'react'
// eslint-disable-next-line import/no-webpack-loader-syntax
import icons from './icons.svg';

export default ({name}) => (
  <svg viewBox='0 0 7 8'>
    <use xlinkHref={`${icons}#${name}`} />
  </svg>
);
