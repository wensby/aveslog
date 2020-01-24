import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext.js';

export function CardBodyRight({ sighting }) {
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  if (sighting.birderId !== account.birder.id) {
    return null;
  }
  
  return (<div className='card-body text-right'>
    <Link to={`/sighting/${sighting.id}`} className='card-link'>
      {t('sighting-item-edit-link')}
    </Link>
  </div>);
}
