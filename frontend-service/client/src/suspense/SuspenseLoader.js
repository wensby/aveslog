import React from 'react';
import './style.scss';

export default () => {
  return (
    <div className='loader-table'>
      <div className='loader-cell' >
        <div className='loader-container'>
          <div className='lds-ring'>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
        </div>
      </div>
    </div>
  );
};
