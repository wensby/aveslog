import React from 'react';
import './FadeInBottom.scss';

export function FadeInBottom({ children }) {
  return (
    <div className='fade-in-bottom'>
      <div>
        {children}
      </div>
    </div>
  );
}
