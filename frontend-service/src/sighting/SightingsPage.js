import React, { useEffect, useContext } from 'react';
import SightingList from './SightingList.js';
import { SightingContext } from './SightingContext';
import { SightingsStats } from './SightingsStats';
import { useTranslation } from 'react-i18next';

export default function SightingsPage() {
  const { sightings, refreshSightings } = useContext(SightingContext);
  const { t } = useTranslation();

  useEffect(() => {
    refreshSightings();
  }, []);

  return (
    <>
      <h1>{t('Sightings')}</h1>
      <SightingsStats sightings={sightings} />
      <SightingList sightings={sightings} />
    </>
  );
}
