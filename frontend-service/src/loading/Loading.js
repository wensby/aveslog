import React from 'react';
import './style.scss';

export default () => {
  return (
    <div className='loading-overlay' >
      <div className='lds-ring-container'>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>);
};
