import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import birdRepository from '../bird/BirdRepository';
import SightingService from './SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useReactRouter } from '../reactRouterHook';

export default function SightingDetails(props) {
  const sightingId = props.match.params.sightingId;
  const [sighting, setSighting] = useState(null);
  const [bird, setBird] = useState(null);
  const { token } = useContext(AuthenticationContext);
  const { t } = useTranslation();
  const sightingService = new SightingService();
  const { history } = useReactRouter();

  const resolveData = async () => {
    const response = await sightingService.fetchSighting(token, sightingId);
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
    const deleted = await sightingService.deleteSighting(token, sightingId);
    if (deleted) {
      history.push('/sighting');
    }
  };

  const name = t(`bird:${bird.binomialName}`, { fallbackLng: [] });

  return (
    <div className='container'>
      <h1>{name}</h1>
      <form onSubmit={event => { event.preventDefault(); }}>
        <button onClick={handleDelete} value='Delete'
          className='btn btn-danger'>{t('delete-sighting-button')}</button>
      </form>
    </div>
  );
}
