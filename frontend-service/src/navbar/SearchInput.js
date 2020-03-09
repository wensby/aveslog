import React, { useContext } from 'react';
import { SearchBarContext } from './SearchBar';
import { useTranslation } from 'react-i18next';
import './SearchInput.scss';

export const SearchInput = React.forwardRef(({ }, ref) => {
  const { query, setQuery } = useContext(SearchBarContext);
  const { t } = useTranslation();

  return <input
    className='search-input'
    ref={ref}
    placeholder={t('Search bird')}
    aria-label={t('Search bird')}
    onChange={e => setQuery(e.target.value)}
    value={query}
  />;
});
