import React from 'react';
import Spinner from './Spinner';
import './LoadingOverlay.scss';

export const LoadingOverlay = () => {
  return (
    <div className='loading-overlay' >
      <Spinner />
    </div>);
};
