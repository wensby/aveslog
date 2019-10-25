import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import SightingService from './SightingService';
import Icon from '../Icon';
import { useBird } from '../bird/BirdHooks';
import { UserContext } from '../authentication/UserContext';
import { useReactRouter } from '../reactRouterHook';

const DeleteButton = ({ onClick }) => {
  const { t } = useTranslation();

  return <button className='button-delete' onClick={onClick}>
    <Icon name='trash' />
    {`${t('delete-sighting-button')}`}
  </button>;
}

export default function SightingDetails({sighting}) {
  const bird = useBird(sighting.birdId);
  const { t } = useTranslation();
  const { getAccessToken } = useContext(UserContext);
  const { history } = useReactRouter();

  if (!bird) {
    return null;
  }

  const handleDelete = async () => {
    const accessToken = await getAccessToken();
    const deleted = await new SightingService().deleteSighting(accessToken, sighting.sightingId);
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
