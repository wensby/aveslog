import React from 'react';
import Icon from '../Icon.js';
import './AdvancedSearchToggle.scss';

export function AdvancedSearchToggle({ active, onChange }) {
  const advancedClick = e => {
    e.preventDefault();
    onChange(!active);
  };
  
  const className = 'advanced-search-icon' + (active ? ' expanded' : '');

  return (
    <div className={className} onClick={advancedClick}>
      <Icon name='down' />
    </div>
  );
}
