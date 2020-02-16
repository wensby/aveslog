import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import './SearchBar.scss';

export const SearchBar = () => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const { t } = useTranslation();
  const inputRef = useRef(null);

  const syncQueryState = event => {
    setQuery(event.target.value);
  }

  const onFormSubmit = event => {
    event.preventDefault();
    history.push(`/bird/search?q=${query}`);
    inputRef.current.blur();
  }

  return (
    <form className='search-bar' onSubmit={onFormSubmit}>
      <div className='text-input'>
        <input ref={inputRef} placeholder={t('Search bird')}
          aria-label='Search bird' onChange={syncQueryState} value={query} />
        <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
      </div>
      <SearchButton expanded={query || advanced} />
    </form>
  );
};

const SearchButton = ({ expanded }) => {
  const { t } = useTranslation();
  const className = expanded ? 'expanded' : null;
  return <button className={className} type='submit'>{t('Search')}</button>;
}
