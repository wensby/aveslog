import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import DetailedSightingCard from './DetailedSightingCard';

export default function SightingSuccess({ sighting, stats }) {
  const { t } = useTranslation();

  return (
    <div>
      <h1 className='success-text'>{t('sighting-success')}</h1>
      <div className='bounce-in-right'>
        <DetailedSightingCard sighting={sighting} />
      </div>
      <Link to={'/sighting'}>{t('sightings-link')}</Link>
    </div>
  );
}
