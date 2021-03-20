import React, { useState, useEffect, useContext } from 'react';
import { SightingsList } from './SightingsList.js';
import { SightingsWeekGraph } from 'generic/SightingsWeekGraph.js';
import { SightingsSectionContext } from './SightingsSection';

const SightingsSectionList = () => {
  const { sightings, year, unique } = useContext(SightingsSectionContext);
  const [displayedSightings, setDisplayedSightings] = useState(sightings);

  useEffect(() => {
    var result = [...sightings];
    if (year !== null) {
      result = result.filter(s => new Date(s.date).getFullYear() === year);
    }
    if (unique) {
      result = getUnique(result);
    }
    setDisplayedSightings(result)
  }, [sightings, year, unique]);

  return (
  <>
  <SightingsWeekGraph sightings={displayedSightings} />
  <SightingsList sightings={displayedSightings} />
  </>
  );
};

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

export { SightingsSectionList };
