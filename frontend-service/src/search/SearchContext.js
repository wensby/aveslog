import React, { useState, useRef, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import { usePosition } from 'usePosition.js';

export const SearchContext = React.createContext();

export const SearchProvider = ({children}) => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const [positionActive, setPositionActive] = useState(false);
  const [position, setPosition] = useState(null);
  const inputRef = useRef(null);
  const { latitude, longitude, error } = usePosition(positionActive);
  const searchFormRef = useRef();
  const disabled = positionActive && !position;

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
    if (!disabled) {
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
  };

  const clear = () => {
    setQuery('');
    setPosition(null);
    setPositionActive(false);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const contextValues = {
    disabled,
    dirty: query || positionActive,
    setQuery,
    query,
    advanced,
    setAdvanced,
    clear,
    position,
    setPosition,
    positionActive,
    setPositionActive,
    submit,
    inputRef,
    searchFormRef,
  };

  return (
    <SearchContext.Provider value={contextValues}>
      {children}
    </SearchContext.Provider>
  );
};
