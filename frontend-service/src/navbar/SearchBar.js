import React, { useState, useRef, useEffect, useContext } from 'react';
import { useHistory } from "react-router-dom";
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import { ClearSearchButton } from './ClearSearchButton';
import { usePosition } from '../usePosition.js';
import { AdvancedSearchSection } from './AdvancedSearchSection.js';
import { SearchInput } from './SearchInput.js';
import { SearchButton } from './SearchButton.js';
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
    dirty: query || positionActive,
    setQuery,
    query,
    advanced,
    setAdvanced,
    clear,
    position,
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
            <SearchInput ref={inputRef} />
            <TextInputRightOverlay />
          </div>
          <SearchButton />
        </div>
      </form>
    </SearchBarContext.Provider>
  );
};

const TextInputRightOverlay = () => {
  const { advanced, setAdvanced, dirty } = useContext(SearchBarContext);
  return (
    <div className='right'>
      {dirty && <ClearSearchButton />}
      <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
    </div>
  );
};
