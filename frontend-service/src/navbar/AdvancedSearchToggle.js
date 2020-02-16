import React from 'react';
import Icon from '../Icon.js';
import './AdvancedSearchToggle.scss';

export const AdvancedSearchToggle = ({ active, onChange }) => {
  const click = e => {
    e.preventDefault();
    onChange(!active);
  };
  
  const className = 'advanced-search-toggle' + (active ? ' expanded' : '');

  return (
    <div className={className} onClick={click}>
      <Icon name='down' />
    </div>
  );
};
