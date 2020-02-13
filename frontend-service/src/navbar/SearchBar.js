import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import './SearchBar.scss';

export const SearchBar = () => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const [searchButtonVisible, setSearchButtonVisible] = useState(false);
  const { t } = useTranslation();
  const inputRef = useRef(null);

  const syncQueryState = event => {
    setQuery(event.target.value);
  }

  useEffect(() => {
    if (query || advanced) {
      setSearchButtonVisible(true);
    }
    else {
      setSearchButtonVisible(false);
    }
  }, [query, advanced]);

  const onFormSubmit = event => {
    event.preventDefault();
    history.push(`/bird/search?q=${query}`);
    inputRef.current.blur();
  }

  return (
    <form onSubmit={onFormSubmit}>
      <div className='search-bar'>
        <input ref={inputRef} className='form-input' placeholder={t('Search bird')}
          aria-label='Search bird' onChange={syncQueryState} value={query} />
        <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
        <button className={searchButtonVisible ? 'expanded' : ''} type='submit'>{t('Search')}</button>
      </div>
    </form>
  );
};
