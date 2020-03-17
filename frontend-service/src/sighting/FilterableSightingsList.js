import React, { useState, useEffect } from 'react';
import { SightingsFilter } from './SightingsFilter';
import { SightingsStats } from './SightingsStats';
import { SightingList } from './SightingList.js';

export const FilterableSightingsList = ({ sightings }) => {
  const [filteredSightings, setFilteredSightings] = useState([]);
  const [yearFilter, setYearFilter] = useState(null);

  useEffect(() => {
    var filtered = sightings;
    if (yearFilter !== null) {
      filtered = filtered
        .filter(s => new Date(s.date).getFullYear() === yearFilter);
    }
    setFilteredSightings(filtered);
  }, [sightings, yearFilter]);

  return <>
    <SightingsFilter sightings={sightings} selectedYear={yearFilter} onYearChange={setYearFilter} />
    <SightingsStats sightings={filteredSightings} />
    <SightingList sightings={filteredSightings} />
  </>;
};
