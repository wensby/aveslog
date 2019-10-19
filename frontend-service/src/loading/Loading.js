import React from 'react';
import './style.scss';
import Spinner from './Spinner';

export default () => {
  return (
    <div className='loading-overlay' >
      <Spinner />
    </div>);
};
