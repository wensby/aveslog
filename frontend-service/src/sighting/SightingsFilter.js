import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { FilterYearOption } from './FilterYearOption';
import './SightingsFilter.scss';

export function SightingsFilter({ sightings, selectedYear, onYearChange }) {
  const [years, setYears] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    if (sightings) {
      const allYears = sightings.map(sighting => new Date(sighting.date).getFullYear());
      const uniqueYears = allYears.filter((item, i, r) => r.indexOf(item) === i);
      uniqueYears.sort();
      setYears(uniqueYears);
    }
  }, [sightings]);

  return (
    <div className='sightings-filter'>
      <span>{t('filter-label') + ': '}</span>
      <FilterYearOption year={null} yearFilter={selectedYear} onClick={onYearChange} />
      {years.map(year => <FilterYearOption year={year} yearFilter={selectedYear} onClick={onYearChange} key={year} />)}
    </div>
  );
}
