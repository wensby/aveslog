import React from 'react';
import Icon from '../Icon.js';

export function AdvancedSearchToggle({ active, onChange }) {
  const advancedClick = e => {
    e.preventDefault();
    onChange(!active);
  };
  
  const className = 'search-advanced-icon' + (active ? ' expanded' : '');

  return (
    <div className={className} onClick={advancedClick}>
      <Icon name='down' />
    </div>
  );
}
