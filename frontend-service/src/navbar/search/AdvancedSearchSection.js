import React, { useContext } from 'react';
import { SearchContext } from './SearchBar.js';
import { useTranslation } from 'react-i18next';
import { Spinner } from 'generic/Spinner';
import './AdvancedSearchSection.scss';

export const AdvancedSearchSection = () => {
  const { advanced, positionActive } = useContext(SearchContext);
  const classNames = ['advanced-search-section'];

  if (advanced) {
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

const SightedNearbyFormGroup = () => {
  const { t } = useTranslation();

  return (
    <div className='sighted-nearby-group'>
      <SightedNearbyCheckbox />
      <label htmlFor='positionCheckbox'>{t('search-sighted-nearby-label')}</label>
    </div>
  );
};

const SightedNearbyCheckbox = () => {
  const { positionActive, setPositionActive, position } = useContext(SearchContext);
  const loading = positionActive && !position;

  const handleChange = e => {
    setPositionActive(e.target.checked);
  }
  
  if (loading) {
    return <div><Spinner /></div>;
  }
  else {
    return <input
      id='positionCheckbox'
      type='checkbox'
      checked={positionActive}
      onChange={handleChange} />;
  }
}
