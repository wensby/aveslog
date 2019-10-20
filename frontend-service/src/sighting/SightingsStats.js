import React from 'react';
import { useTranslation } from 'react-i18next';
import { StatCard } from "./StatCard";

export function SightingsStats({ sightings }) {
  const { t } = useTranslation();
  return (
    <div className='sighting-stats'>
      <StatCard label={t('total-label')} stat={sightings.length} />
      <StatCard label={t('unique-label')} stat={countUniqueBirds(sightings)} />
    </div>
  );
}

export function countUniqueBirds(sightings) {
  return new Set(sightings.map(sighting => sighting.birdId)).size;
}
