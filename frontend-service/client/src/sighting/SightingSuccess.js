import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { DetailedSightingCard } from './DetailedSightingCard';
import { BounceInRight } from '../component/BounceInRight';
import './SightingSuccess.scss';

export const SightingSuccess = ({ sighting }) => {
  const { t } = useTranslation();

  return (
    <div className='sighting-success'>
      <h1 className='success-text'>{t('sighting-success')}</h1>
      <BounceInRight>
        <DetailedSightingCard sighting={sighting} />
      </BounceInRight>
      <Link to={'/sighting'}>{t('sightings-link')}</Link>
    </div>
  );
};
