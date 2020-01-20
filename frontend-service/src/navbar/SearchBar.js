import React, { useState } from 'react';
import { useReactRouter } from '../reactRouterHook';
import { useTranslation } from 'react-i18next';
import Icon from '../Icon.js';

export function SearchBar({}) {
  const { history } = useReactRouter();
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

function AdvancedSearchToggle({ active, onChange }) {
  const advancedClick = e => {
    e.preventDefault();
    onChange(!active);
  };

  const className = 'search-advanced-icon' + (active ? ' expanded' : '');

  return (
    <div className={className} onClick={advancedClick}>
      <Icon name='down' />
    </div>
  );
}
