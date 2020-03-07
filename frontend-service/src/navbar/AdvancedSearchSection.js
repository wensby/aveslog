import React, { useContext } from 'react';
import { SearchBarContext } from './SearchBar.js';
import './AdvancedSearchSection.scss';

export const AdvancedSearchSection = () => {
  const { advanced, positionActive, setPositionActive } = useContext(SearchBarContext);

  const handleChange = e => {
    setPositionActive(e.target.checked);
  }

  const classNames = ['advanced-search-section'];
  if (advanced) {
    classNames.push('active');
  }
  if (positionActive) {
    classNames.push('dirty');
  }

  return (
    <div className={classNames.join(' ')}>
      <div className='sighted-nearby-group'>
        <input id='positionCheckbox' type='checkbox' onChange={handleChange} checked={positionActive} />
        <label htmlFor='positionCheckbox'>Sighted near my location</label>
      </div>
    </div>
  );
};
