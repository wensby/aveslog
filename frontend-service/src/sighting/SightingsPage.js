import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuthenticatedAccountSightings } from '../useAuthenticatedAccountSightings';
import { FilterableSightingsList } from './FilterableSightingsList';

export default function SightingsPage() {
  const sightings = useAuthenticatedAccountSightings();
  const { t } = useTranslation();

  return (
    <>
      <h1>{t('Sightings')}</h1>
      <FilterableSightingsList sightings={sightings} />
    </>
  );
}
