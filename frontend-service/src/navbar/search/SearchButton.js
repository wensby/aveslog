import React, { useContext } from 'react';
import { SearchContext } from '../../search/SearchContext';
import { useTranslation } from 'react-i18next';
import { SearchSubmitButton } from 'search/SearchSubmitButton';
import './SearchButton.scss';

export const SearchButton = () => {
  const { dirty, advanced, disabled } = useContext(SearchContext);
  const { t } = useTranslation();

  const classNames = ['search-button'];

  if (dirty || advanced || disabled) {
    classNames.push('expanded');
  }

  const className = classNames.join(' ');

  return (
    <SearchSubmitButton className={className}>
      {t('Search')}
    </SearchSubmitButton>
  );
};
