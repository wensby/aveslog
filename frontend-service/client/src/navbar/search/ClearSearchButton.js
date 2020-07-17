import React, { useContext } from 'react';
import Icon from 'Icon.js';
import './ClearSearchButton.scss';
import { SearchContext } from '../../search/SearchContext.js';

export const ClearSearchButton = () => {
  const { clear } = useContext(SearchContext);
  return (
    <div className='clear-search-button' onClick={clear}>
      <Icon name='cross' viewBox='0 0 1 1'/>
    </div>
  );
};
