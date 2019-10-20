import React from 'react';

export function StatCard({ label, stat }) {
  return (
    <div className='stat-card'>
      <div>{label}</div>
      <div className='stat'>{stat}</div>
    </div>
  );
}
