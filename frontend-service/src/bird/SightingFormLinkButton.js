import React from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import Icon from '../Icon.js';
import './SightingFormLinkButton.scss'

export function SightingFormLinkButton({ bird }) {
  const { t } = useTranslation();
  return (
    <div className='sighting-form-link-button'>
      <NewBirdSightingLink bird={bird}>
        <Icon name='eye' />
        <span>{t('add-sighting-link')}</span>
      </NewBirdSightingLink>
    </div>
  );
}
