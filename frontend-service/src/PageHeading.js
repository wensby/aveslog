import React from 'react';
import './PageHeading.scss';

export function PageHeading({ children }) {
  return <h1 className='page-heading'>{children}</h1>;
}
