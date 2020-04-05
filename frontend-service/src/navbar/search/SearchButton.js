import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { SearchContext } from './SearchContext';
import './SearchButton.scss';

export const SearchButton = () => {
  const { dirty, advanced, disabled } = useContext(SearchContext);
  const { t } = useTranslation();

  const classNames = ['search-button'];
  
  if (dirty || advanced || disabled) {
    classNames.push('expanded');
  }
  
  const className = classNames.join(' ');
  
  return <button disabled={disabled} className={className} type='submit'>{t('Search')}</button>;
};
