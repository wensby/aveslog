import React from 'react';
import SightingList from './SightingList.js';
import { SightingsStats } from './SightingsStats';
import { useTranslation } from 'react-i18next';
import { useAuthenticatedAccountSightings } from '../useAuthenticatedAccountSightings';

export default function SightingsPage() {
  const { t } = useTranslation();
  const sightings = useAuthenticatedAccountSightings();

  return (
    <>
      <h1>{t('Sightings')}</h1>
      <SightingsStats sightings={sightings} />
      <SightingList sightings={sightings} />
    </>
  );
}
