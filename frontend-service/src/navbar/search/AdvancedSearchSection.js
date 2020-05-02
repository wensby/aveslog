import React, { useContext } from 'react';
import { SearchContext } from '../../search/SearchContext.js';
import { SightedNearbyFormGroup } from './SightedNearbyFormGroup.js';
import './AdvancedSearchSection.scss';

export const AdvancedSearchSection = ({active}) => {
  const { positionActive } = useContext(SearchContext);
  const classNames = ['advanced-search-section'];

  if (active) {
    classNames.push('active');
  }
  if (positionActive) {
    classNames.push('dirty');
  }

  return (
    <div className={classNames.join(' ')}>
      <SightedNearbyFormGroup />
    </div>
  );
};
