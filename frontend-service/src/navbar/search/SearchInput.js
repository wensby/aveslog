import React, { useContext } from 'react';
import { SearchBarContext } from './SearchBar';
import { useTranslation } from 'react-i18next';
import './SearchInput.scss';

export const SearchInput = React.forwardRef((props, ref) => {
  const { query, setQuery } = useContext(SearchBarContext);
  const { t } = useTranslation();

  const label = t('Search bird');

  const handleChange = event => {
    setQuery(event.target.value);
  };

  return <input className='search-input' ref={ref} placeholder={label}
    aria-label={label} onChange={handleChange} value={query}/>;
});
