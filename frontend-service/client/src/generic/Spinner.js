import React from 'react';
import './Spinner.scss';

export const Spinner = ({onClick}) => {
  return (
    <div className='spinner' onClick={onClick}>
      <div />
    </div>
  );
};
