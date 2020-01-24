import React from 'react';
import { useTranslation } from 'react-i18next';

export function FilterYearOption({ year, yearFilter, onClick }) {
  const { t } = useTranslation();
  return <button disabled={yearFilter === year} className={yearFilter === year ? 'selected' : ''} onClick={e => onClick(year)}>
    {year || t('year-filter-all')}
  </button>;
}
