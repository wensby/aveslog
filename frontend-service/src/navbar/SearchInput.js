import React from 'react';
import { useTranslation } from 'react-i18next';
import './SearchInput.scss';

export const SearchInput = React.forwardRef(({ value, onChange }, ref) => {
  const { t } = useTranslation();

  return <input
    className='search-input'
    ref={ref}
    placeholder={t('Search bird')}
    aria-label={t('Search bird')}
    onChange={e => onChange(e.target.value)}
    value={value}
  />;
});
