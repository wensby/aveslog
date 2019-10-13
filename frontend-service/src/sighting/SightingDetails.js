import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository';
import SightingService from './SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
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
  const { getAccessToken } = useContext(AuthenticationContext);
  const { t } = useTranslation();
  const sightingService = new SightingService();
  const { history } = useReactRouter();

  const resolveData = async () => {
    const accessToken = await getAccessToken();
    const response = await sightingService.fetchSighting(accessToken, sightingId);
    if (response.status == 'success') {
      const sighting = response.result;
      const bird = await birdRepository.getBird(sighting.birdId);
      setSighting(sighting);
      setBird(bird);
    }
  }

  useEffect(() => {
    resolveData();
  }, []);

  if (!sighting || !bird) {
    return null;
  }

  const handleDelete = async () => {
    const accessToken = await getAccessToken();
    const deleted = await sightingService.deleteSighting(accessToken, sightingId);
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
