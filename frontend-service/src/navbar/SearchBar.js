import React, { useState, useRef, useContext, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import { ClearSearchButton } from './ClearSearchButton';
import { usePosition } from '../usePosition.js';
import { AdvancedSearchSection } from './AdvancedSearchSection.js';
import { SearchInput } from './SearchInput.js';
import './SearchBar.scss';

export const SearchBarContext = React.createContext();

export const SearchBar = () => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const [positionActive, setPositionActive] = useState(false);
  const [position, setPosition] = useState(null);
  const inputRef = useRef(null);
  const { latitude, longitude, error } = usePosition(positionActive);
  const searchFormRef = useRef()

  const onDocumentClick = event => {
    if (searchFormRef && !searchFormRef.current.contains(event.target)) {
      setAdvanced(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', onDocumentClick, true);
    return () => document.removeEventListener('click', onDocumentClick);
  }, []);

  useEffect(() => {
    if (latitude && longitude) {
      setPosition([latitude, longitude])
    }
    else {
      setPosition(null);
    }
  }, [latitude, longitude]);

  useEffect(() => {
    if (error) {
      setPositionActive(false);
      setPosition(null);
    }
  }, [error]);

  const submit = event => {
    event.preventDefault();
    const qParts = [];
    if (query) {
      qParts.push(`"${query}"`)
    }
    if (position) {
      const [latitude, longitude] = position;
      qParts.push(`position:${latitude},${longitude};r=10`)
    }
    history.push(`/bird/search?q=${qParts.join('+')}`);
    setAdvanced(false);
    inputRef.current.blur();
  }

  const clear = () => {
    setQuery('');
    setPosition(null);
    setPositionActive(false);
    inputRef.current.focus();
  }

  const contextValues = {
    dirty: query || advanced || positionActive,
    query,
    advanced,
    clear,
    setPosition,
    positionActive,
    setPositionActive
  }

  return (
    <SearchBarContext.Provider value={contextValues}>
      <form ref={searchFormRef} className='search-bar' onSubmit={submit}>
        <AdvancedSearchSection />
        <div className='simple-search-section'>
          <div className='text-input'>
            <SearchInput ref={inputRef} value={query} onChange={setQuery} />
            <div className='right'>
              {(position || query) && <ClearSearchButton />}
              <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
            </div>
          </div>
          <SearchButton />
        </div>
      </form>
    </SearchBarContext.Provider>
  );
};

const SearchButton = () => {
  const { dirty } = useContext(SearchBarContext);
  const { t } = useTranslation();
  const className = (dirty) ? 'expanded' : null;
  return <button className={className} type='submit'>{t('Search')}</button>;
};
