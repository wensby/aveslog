import React from 'react';
import './StatCard.scss';

export const StatCard = ({ label, stat }) => {
  return (
    <div className='stat-card'>
      <div>{label}</div>
      <div className='stat'>{stat}</div>
    </div>
  );
};
