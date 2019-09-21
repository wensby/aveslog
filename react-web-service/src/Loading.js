import React from 'react';
import './loading.css';

export default () => {
  return (
    <div className='loading-overlay' >
      <div className='lds-ring'>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>);
};
