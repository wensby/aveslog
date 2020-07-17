import React, { useContext, useState } from 'react';
import { ClearSearchButton } from 'navbar/search/ClearSearchButton';
import { AdvancedSearchSection } from 'navbar/search/AdvancedSearchSection.js';
import { SearchInput } from 'navbar/search/SearchInput.js';
import { SearchContext } from 'search/SearchContext.js';
import { useTranslation } from 'react-i18next';
import { SearchSubmitButton } from 'search/SearchSubmitButton';
import Icon from 'Icon';
import './SearchForm.scss';

export const SearchForm = () => {
  const { submit, dirty } = useContext(SearchContext);
  const [extended, setExtended] = useState(false);

  const handleSubmit = event => {
    event.preventDefault();
    if (dirty) {
      submit();
    }
  };

  return (
    <form className={searchFormClassName(extended, dirty)} onSubmit={handleSubmit}>
      <SimpleInputSection />
      <AdvancedSearchSection />
      <ExtendedSearchToggle extended={extended} onChange={setExtended} />
    </form>
  );
};

const searchFormClassName = (extended, dirty) => {
  const classNames = ['search'];
  if (extended) {
    classNames.push('extended');
  }
  if (dirty) {
    classNames.push('dirty');
  }
  return classNames.join(' ');
};

const SimpleInputSection = () => {
  const { query, positionActive } = useContext(SearchContext);
  return (
    <div className='simple-input'>
      <SearchInput ref={null}>
        <div className='right'>
          {(query || positionActive) && <ClearSearchButton />}
        </div>
      </SearchInput>
      <SearchSubmitButton>></SearchSubmitButton>
    </div>
  );
}

const ExtendedSearchToggle = ({ extended, onChange }) => {
  const { t } = useTranslation();
  return (
    <div className='extended-search-toggle' onClick={() => onChange(!extended)} >
      {t('extended-search-label')}
      <Icon name='down' />
    </div>
  );
};
