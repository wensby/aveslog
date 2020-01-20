import React, { useState, useEffect, useContext } from 'react';
import { UserContext }  from '../authentication/UserContext';
import SightingService from './SightingService';
import { DetailedSightingCard } from './DetailedSightingCard';
import { useTranslation } from 'react-i18next';
import Icon from '../Icon';
import { useHistory } from "react-router-dom";

export function SightingPage({match}) {
  const sightingId = match.params.sightingId;
  const [sighting, setSighting] = useState(null);
  const { getAccessToken, account } = useContext(UserContext);
  const sightingService = new SightingService();
  const history = useHistory();

  useEffect(() => {
    const resolveSighting = async () => {
      const accessToken = await getAccessToken();
      const response = await sightingService.fetchSighting(accessToken, sightingId);
      if (response.status === 200) {
        const sighting = await response.json();
        setSighting(sighting);
      }
    }
    resolveSighting();
  }, [sightingId]);

  const handleDelete = async () => {
    const accessToken = await getAccessToken();
    const deleted = await new SightingService().deleteSighting(accessToken, sighting.id);
    if (deleted) {
      history.push('/sighting');
    }
  };

  if (!sighting) {
    return null;
  }

  const renderDelete = () => {
    if (account && account.birder.id === sighting.birderId) {
      return <form onSubmit={event => { event.preventDefault(); }}>
      <DeleteButton onClick={handleDelete} />
    </form>;
    }
    else {
      return null;
    }
  };

  return (
    <>
      <DetailedSightingCard sighting={sighting}/>
      {renderDelete()}
    </>
  );
}

const DeleteButton = ({ onClick }) => {
  const { t } = useTranslation();

  return <button className='button-delete' onClick={onClick}>
    <Icon name='trash' />
    {`${t('delete-sighting-button')}`}
  </button>;
}
