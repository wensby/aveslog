import React, { useState, useRef, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import { ClearSearchButton } from './ClearSearchButton';
import './SearchBar.scss';

export const SearchBarContext = React.createContext();

export const SearchBar = () => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const inputRef = useRef(null);

  const submit = event => {
    event.preventDefault();
    history.push(`/bird/search?q=${query}`);
    inputRef.current.blur();
  }

  const clear = () => {
    setQuery('');
    inputRef.current.focus();
  }

  return (
    <SearchBarContext.Provider value={{ query, advanced, clear }}>
      <form className='search-bar' onSubmit={submit}>
        <div className='text-input'>
          <SearchInput ref={inputRef} value={query} onChange={setQuery} />
          <div className='right'>
            {query && <ClearSearchButton />}
            <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
          </div>
        </div>
        <SearchButton />
      </form>
    </SearchBarContext.Provider>
  );
};

const SearchInput = React.forwardRef(({ value, onChange }, ref) => {
  const { t } = useTranslation();

  return <input
    className='search-input'
    ref={ref}
    placeholder={t('Search bird')}
    aria-label={t('Search bird')}
    onChange={e => onChange(e.target.value)}
    value={value} />;
});

const SearchButton = () => {
  const { query, advanced } = useContext(SearchBarContext);
  const { t } = useTranslation();
  const className = (query || advanced) ? 'expanded' : null;
  return <button className={className} type='submit'>{t('Search')}</button>;
};
