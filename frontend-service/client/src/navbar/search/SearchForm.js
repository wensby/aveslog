import React, { useContext } from 'react';
import { SearchInput } from './SearchInput.js';
import { SearchButton } from './SearchButton.js';
import { SearchBarContext } from './SearchBar';
import { ClearSearchButton } from './ClearSearchButton';
import './SearchForm.scss';

export const SearchForm = () => {
  const { searchFormRef, submit } = useContext(SearchBarContext);

  const handleSubmit = event => {
    event.preventDefault();
    submit();
  };

  return (
    <form ref={searchFormRef} className='search-form' onSubmit={handleSubmit}>
      <SimpleSearchSection />
    </form>
  );
};

export const SimpleSearchSection = () => {
  const { inputRef } = useContext(SearchBarContext);

  return (
    <div className='simple-search-section'>
      <div className='text-input'>
        <SearchInput ref={inputRef}>
          <TextInputRightOverlay />
        </SearchInput>
      </div>
      <SearchButton />
    </div>
  );
}


const TextInputRightOverlay = () => {
  const { dirty } = useContext(SearchBarContext);

  return (
    <div className='right'>
      {dirty && <ClearSearchButton />}
    </div>
  );
};
