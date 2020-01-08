import React, { useState, useEffect } from 'react';
import { SightingList } from './SightingList.js';
import { SightingsStats } from './SightingsStats';
import { useTranslation } from 'react-i18next';
import { useAuthenticatedAccountSightings } from '../useAuthenticatedAccountSightings';

export default function SightingsPage() {
  const [filteredSightings, setFilteredSightings] = useState([]);
  const [yearFilter, setYearFilter] = useState(null);
  const sightings = useAuthenticatedAccountSightings();
  const { t } = useTranslation();

  useEffect(() => {
    if (yearFilter === null) {
      setFilteredSightings(sightings);
    }
    else {
      setFilteredSightings(sightings.filter(sighting =>
        new Date(sighting.date).getFullYear() == yearFilter
      ));
    }
  }, [sightings, yearFilter]);

  return (
    <>
      <h1>{t('Sightings')}</h1>
      <SightingsFilter sightings={sightings} selectedYear={yearFilter} onYearChange={setYearFilter} />
      <SightingsStats sightings={filteredSightings} />
      <SightingList sightings={filteredSightings} />
    </>
  );
}

function SightingsFilter({ sightings, selectedYear, onYearChange }) {
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

  return <div class='sightings-filter'>
    <span>{t('filter-label') + ': '}</span>
    <FilterYearOption year={null} yearFilter={selectedYear} onClick={onYearChange} />
    {years.map(year => <FilterYearOption year={year} yearFilter={selectedYear} onClick={onYearChange} />)}
  </div>;
}

function FilterYearOption({ year, yearFilter, onClick }) {
  const { t } = useTranslation();

  return <button
    disabled={yearFilter === year}
    className={yearFilter === year ? 'selected' : ''}
    onClick={e => onClick(year)}>
    {year || t('year-filter-all')}
  </button>;
}
