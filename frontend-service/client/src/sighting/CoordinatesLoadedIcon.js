import React from 'react';

export function CoordinatesLoadedIcon({ display }) {
  if (display) {
    return <div className='loaded-icon'>✓</div>;
  }
  return null;
}
