import React, { useContext } from 'react';
import Icon from '../Icon.js';
import './ClearSearchButton.scss';
import { SearchBarContext } from './SearchBar.js';

export const ClearSearchButton = () => {
  const { clear } = useContext(SearchBarContext);
  return (
    <div className='clear-search-button' onClick={clear}>
      <Icon name='cross' viewBox='0 0 1 1'/>
    </div>
  );
};
