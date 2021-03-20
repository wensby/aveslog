import React, { useState, useEffect, useContext } from 'react';
import { SightingsSectionFilter } from './SightingsSectionFilter.js';
import { useTranslation } from 'react-i18next';
import { DisplayMode } from './DisplayMode.js';
import { SightingsSectionList } from './SightingsSectionList';
import './SightingsSection.scss';

export const SightingsSectionContext = React.createContext();

export const SightingsSection = ({ sightings }) => {
  const [year, setYear] = useState(null);
  const [unique, setUnique] = useState(false);

  const contextValue = {
    sightings,
    year,
    setYear,
    unique,
    setUnique,
  };

  return (
    <SightingsSectionContext.Provider value={contextValue}>
      <section className='sightings'>
        <SightingsSectionFilter />
        <SightingsSectionDisplayMode />
        <SightingsSectionList />
      </section>
    </SightingsSectionContext.Provider>
  );
};

const SightingsSectionDisplayMode = () => {
  const { sightings, year, unique, setUnique } = useContext(SightingsSectionContext);
  const [totalCount, setTotalCount] = useState(0);
  const [uniqueCount, setUniqueCount] = useState(0);
  const { t } = useTranslation();

  useEffect(() => {
    const filtered = sightings.filter(s => !year || new Date(s.date).getFullYear() === year);
    setTotalCount(filtered.length);
    setUniqueCount(countUniqueBirds(filtered));
  }, [sightings, year, unique]);

  return (
    <div className='display-settings'>
      <DisplayMode label={t('total-label')} stat={totalCount} selected={!unique} onClick={() => setUnique(false)} />
      <DisplayMode label={t('unique-label')} stat={uniqueCount} selected={unique} onClick={() => setUnique(true)} />
    </div>
  );
};

function countUniqueBirds(sightings) {
  return new Set(sightings.map(sighting => sighting.birdId)).size;
}
