import React, { useState, useEffect } from 'react';
import { SightingList } from './SightingList.js';
import { SightingsStats } from './SightingsStats';
import { SightingsFilter } from './SightingsFilter';

export function FilterableSightingsList({ sightings }) {
  const [filteredSightings, setFilteredSightings] = useState([]);
  const [yearFilter, setYearFilter] = useState(null);

  useEffect(() => {
    if (yearFilter === null) {
      setFilteredSightings(sightings);
    }
    else {
      setFilteredSightings(sightings.filter(sighting => new Date(sighting.date).getFullYear() === yearFilter));
    }
  }, [sightings, yearFilter]);
  return <>
    <SightingsFilter sightings={sightings} selectedYear={yearFilter} onYearChange={setYearFilter} />
    <SightingsStats sightings={filteredSightings} />
    <SightingList sightings={filteredSightings} />
  </>;
}
