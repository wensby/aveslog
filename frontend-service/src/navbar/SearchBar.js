import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';

export function SearchBar({}) {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const { t } = useTranslation();

  const syncQueryState = event => {
    setQuery(event.target.value);
  }

  const onFormSubmit = event => {
    event.preventDefault();
    history.push(`/bird/search?q=${query}`);
    setQuery('');
  }

  return (
    <form onSubmit={onFormSubmit}>
      <div className='search-bar'>
        <input className='form-input' placeholder={t('Search bird')} 
          aria-label='Search bird' onChange={syncQueryState} value={query} />
        <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
        <button type='submit'>{t('Search')}</button>
      </div>
    </form>
  );
}
