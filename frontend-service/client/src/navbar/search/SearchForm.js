import React, { useContext } from 'react';
import { AdvancedSearchSection } from './AdvancedSearchSection.js';
import { SearchInput } from './SearchInput.js';
import { SearchButton } from './SearchButton.js';
import { SearchBarContext } from './SearchBar';
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import { ClearSearchButton } from './ClearSearchButton';
import './SearchForm.scss';

export const SearchForm = () => {
  const { searchFormRef, submit, advanced } = useContext(SearchBarContext);

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
  const { advanced, setAdvanced, dirty } = useContext(SearchBarContext);

  return (
    <div className='right'>
      {dirty && <ClearSearchButton />}
    </div>
  );
};
