import React, { useContext } from 'react';
import { AdvancedSearchToggle } from './AdvancedSearchToggle';
import { ClearSearchButton } from './ClearSearchButton';
import { AdvancedSearchSection } from './AdvancedSearchSection.js';
import { SearchInput } from './SearchInput.js';
import { SearchButton } from './SearchButton.js';
import { SearchContext } from './SearchContext.js';
import './SearchForm.scss';

export const SearchForm = () => {
  const { submit, searchFormRef } = useContext(SearchContext);
  return (
    <form ref={searchFormRef} className='search-form' onSubmit={submit}>
      <AdvancedSearchSection />
      <SimpleSearchSection />
    </form>
  );
};

export const SplashSearchForm = () => {
  const { submit, searchFormRef } = useContext(SearchContext);
  return (
    <form ref={searchFormRef} className='search-form' onSubmit={submit}>
      <SimpleSearchSection />
      <AdvancedSearchSection />
    </form>
  );
}

export const SimpleSearchSection = () => {
  const { inputRef } = useContext(SearchContext);
  return (
    <div className='simple-search-section'>
      <div className='text-input'>
        <SearchInput ref={inputRef} />
        <TextInputRightOverlay />
      </div>
      <SearchButton />
    </div>
  );
}

const TextInputRightOverlay = () => {
  const { advanced, setAdvanced, dirty } = useContext(SearchContext);
  return (
    <div className='right'>
      {dirty && <ClearSearchButton />}
      <AdvancedSearchToggle active={advanced} onChange={setAdvanced} />
    </div>
  );
};
