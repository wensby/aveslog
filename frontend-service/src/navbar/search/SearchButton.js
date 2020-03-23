import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { SearchBarContext } from './SearchBar';
import './SearchButton.scss';

export const SearchButton = () => {
  const { dirty, advanced, disabled } = useContext(SearchBarContext);
  const { t } = useTranslation();

  const classNames = ['search-button'];
  
  if (dirty || advanced || disabled) {
    classNames.push('expanded');
  }
  
  const className = classNames.join(' ');
  
  return <button disabled={disabled} className={className} type='submit'>{t('Search')}</button>;
};
