import React, { useContext } from 'react';
import { SearchContext } from './SearchContext';

export const SearchSubmitButton = ({ children, className }) => {
  const { disabled } = useContext(SearchContext);

  return (
    <button type='submit' disabled={disabled} className={className}>
      {children}
    </button>
  );
};
