import React, { useState } from 'react';
import { useReactRouter } from '../reactRouterHook';
import { useTranslation } from 'react-i18next';

export function SearchBar({}) {
  const { history } = useReactRouter();
  const [query, setQuery] = useState('');
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
        <button type='submit'>{t('Search')}</button>
      </div>
    </form>
  );
}
