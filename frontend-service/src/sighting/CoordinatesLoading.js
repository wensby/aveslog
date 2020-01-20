import React from 'react';
import Spinner from '../loading/Spinner';

export function CoordinatesLoading({ display }) {
  if (display) {
    return <Spinner />;
  }
  return null;
}
