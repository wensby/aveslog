import React, { useState, useEffect } from 'react';
import { SightingsFilter } from './SightingsFilter';
import { SightingsList } from './SightingsList.js';
import { useTranslation } from 'react-i18next';
import { DisplayMode } from './DisplayMode.js';
import './FilterableSightingsList.scss';

export const FilterableSightingsList = ({ sightings }) => {
  const [filteredSightings, setFilteredSightings] = useState([]);
  const [yearFilter, setYearFilter] = useState(null);
  const [uniqueFilter, setUniqueFilter] = useState(false);
  const { t } = useTranslation();

  useEffect(() => {
    var filtered = sightings;
    if (yearFilter !== null) {
      filtered = filtered
        .filter(s => new Date(s.date).getFullYear() === yearFilter);
    }
    setFilteredSightings(filtered);
  }, [sightings, yearFilter]);

  return <div className='filterable-sightings-list'>
    <SightingsFilter sightings={sightings} selectedYear={yearFilter} onYearChange={setYearFilter} />
    <div className='display-settings'>
      <DisplayMode label={t('total-label')} stat={filteredSightings.length} selected={!uniqueFilter} onClick={() => setUniqueFilter(false)} />
      <DisplayMode label={t('unique-label')} stat={countUniqueBirds(filteredSightings)} selected={uniqueFilter} onClick={() => setUniqueFilter(true)} />
    </div>
    <SightingsList sightings={uniqueFilter ? getUnique(filteredSightings) : filteredSightings} />
  </div>;
};

function countUniqueBirds(sightings) {
  return new Set(sightings.map(sighting => sighting.birdId)).size;
}

const getUnique = sightings => {
  const result = [];
  const map = new Map();
  const copy = [...sightings];
  copy.reverse()
  for (const sighting of copy) {
    if (!map.has(sighting.birdId)) {
      map.set(sighting.birdId, true);
      result.push(sighting);
    }
  }
  return result.reverse();
}

const sightingDateTime = sighting => {
  if (sighting.time) {
    return new Date(`${sighting.date}T${sighting.time}`);
  }
  return new Date(sighting.date);
};
