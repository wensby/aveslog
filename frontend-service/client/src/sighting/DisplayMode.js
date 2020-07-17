import React from 'react';
import './DisplayMode.scss';

export const DisplayMode = ({ label, stat, onClick, selected }) => {
  const classNames = ['display-mode'];
  
  if (selected) {
    classNames.push('selected');
  }

  const handleClick = () => {
    if (!selected) {
      onClick();
    }
  }

  return (
    <div className={classNames.join(' ')} onClick={handleClick}>
      <div>{label}</div>
      <div className='stat'>{stat}</div>
    </div>
  );
};
