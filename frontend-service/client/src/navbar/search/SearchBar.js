import React, { useState, useRef, useEffect, useContext } from 'react';
import { SearchContext } from 'search/SearchContext';
import { SearchForm } from './SearchForm';

export const SearchBarContext = React.createContext();

export const SearchBar = () => {
  const { positionActive, query, disabled, submit: searchSubmit } = useContext(SearchContext);
  const [advanced, setAdvanced] = useState(false);
  const inputRef = useRef(null);
  const searchFormRef = useRef();

  const onDocumentClick = event => {
    const target = event.target;
    if (searchFormRef.current && !searchFormRef.current.contains(target)) {
      setAdvanced(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', onDocumentClick, true);
    return () => document.removeEventListener('click', onDocumentClick);
  }, []);

  const submit = () => {
    if (!disabled) {
      searchSubmit();
      setAdvanced(false);
      inputRef.current.blur();
    }
  };

  const contextValues = {
    dirty: query || positionActive,
    advanced,
    setAdvanced,
    submit,
    inputRef,
    searchFormRef,
  };

  return (
    <SearchBarContext.Provider value={contextValues}>
      <SearchForm />
    </SearchBarContext.Provider>
  );
};
