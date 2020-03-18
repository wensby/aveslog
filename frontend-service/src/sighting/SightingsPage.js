import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuthenticatedAccountSightings } from '../useAuthenticatedAccountSightings';
import { SightingsSection } from './SightingsSection.js';

export default function SightingsPage() {
  const sightings = useAuthenticatedAccountSightings();
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('Sightings')}</h1>
      <SightingsSection sightings={sightings} />
    </div>
  );
}
