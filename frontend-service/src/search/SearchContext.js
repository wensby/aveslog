import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { usePosition } from 'usePosition.js';

const SearchContext = React.createContext();

const SearchProvider = ({ children }) => {
  const history = useHistory();
  const [query, setQuery] = useState('');
  const [positionActive, setPositionActive] = useState(false);
  const [position, setPosition] = useState(null);
  const { latitude, longitude, error } = usePosition(positionActive);
  const disabled = positionActive && !position;

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

  const submit = () => {
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
    }
  };

  const clear = () => {
    setQuery('');
    setPosition(null);
    setPositionActive(false);
  };

  const contextValues = {
    disabled,
    dirty: query || positionActive,
    setQuery,
    query,
    clear,
    position,
    setPosition,
    positionActive,
    setPositionActive,
    submit,
  };

  return (
    <SearchContext.Provider value={contextValues}>
      {children}
    </SearchContext.Provider>
  );
};

export { SearchProvider, SearchContext }
