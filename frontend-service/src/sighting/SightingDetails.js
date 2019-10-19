import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository';
import SightingService from './SightingService';
import { UserContext } from '../authentication/UserContext';
import { useReactRouter } from '../reactRouterHook';
import Icon from '../Icon';

const DeleteButton = ({ onClick }) => {
  const { t } = useTranslation();
  return <button className='button-delete' onClick={onClick}>
    <Icon name='trash' />
    {`${t('delete-sighting-button')}`}
  </button>;
}

export default function SightingDetails(props) {
  const sightingId = props.match.params.sightingId;
  const [sighting, setSighting] = useState(null);
  const [bird, setBird] = useState(null);
  const { getAccessToken } = useContext(UserContext);
  const { t } = useTranslation();
  const { history } = useReactRouter();

  useEffect(() => {
    const resolveData = async () => {
      const accessToken = await getAccessToken();
      const response = await new SightingService().fetchSighting(accessToken, sightingId);
      if (response.status === 'success') {
        const sighting = response.result;
        const bird = await birdRepository.getBird(sighting.birdId);
        setSighting(sighting);
        setBird(bird);
      }
    }
    resolveData();
  }, [getAccessToken, sightingId]);

  if (!sighting || !bird) {
    return null;
  }

  const handleDelete = async () => {
    const accessToken = await getAccessToken();
    const deleted = await new SightingService().deleteSighting(accessToken, sightingId);
    if (deleted) {
      history.push('/sighting');
    }
  };

  const name = t(`bird:${bird.binomialName}`, { fallbackLng: [] });
  const time = `${sighting.date} ${sighting.time ? sighting.time : ''}`;

  return (
    <>
      <h1>{name}</h1>
      <h2>{time}</h2>
      <form onSubmit={event => { event.preventDefault(); }}>
        <DeleteButton onClick={handleDelete} />
      </form>
    </>
  );
}
