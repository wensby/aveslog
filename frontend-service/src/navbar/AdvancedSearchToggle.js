import React, { useContext } from 'react';
import Icon from '../Icon.js';
import { SearchBarContext } from './SearchBar.js';
import './AdvancedSearchToggle.scss';

export const AdvancedSearchToggle = ({ active, onChange }) => {
  const { positionActive } = useContext(SearchBarContext);
  const click = e => {
    e.preventDefault();
    onChange(!active);
  };
  
  const classNames = ['advanced-search-toggle'];
  if (active) {
    classNames.push('expanded');
  }
  if (positionActive) {
    classNames.push('dirty');
  }

  return (
    <div className={classNames.join(' ')} onClick={click}>
      <Icon name='down' />
    </div>
  );
};
