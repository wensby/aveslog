import React from 'react';
import './SighedIndicator.scss';

export const SightedIndicator = ({ date }) => {
  return <div className='sighted-indicator'>{`✓ ${date}`}</div>;
}
