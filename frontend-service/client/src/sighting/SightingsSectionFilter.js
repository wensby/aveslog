import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { FilterYearOption } from './FilterYearOption';
import { SightingsSectionContext } from './SightingsSection';
import './SightingsSectionFilter.scss';

export const SightingsSectionFilter = () => {
  const { sightings, year, setYear } = useContext(SightingsSectionContext);
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
      <FilterYearOption year={null} yearFilter={year} onClick={setYear} />
      {years.map(y => <FilterYearOption year={y} yearFilter={year} onClick={setYear} key={y} />)}
    </div>
  );
};
