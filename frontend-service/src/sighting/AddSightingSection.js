import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import SightingService from './SightingService';
import { UserContext } from '../authentication/UserContext';
import { BirdSection } from "./BirdSection";
import { Label } from "./Label";
import { LocationSection } from "./LocationSection";
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { PageHeading } from 'generic/PageHeading';
import './AddSightingSection.scss';
import { CircledBirdPicture } from 'bird/CircledBirdPicture';

export const AddSightingSection = ({ bird, onSuccess }) => {
  const { t } = useTranslation();
  const { account } = useContext(UserContext);
  const { getAccessToken } = useContext(AuthenticationContext);
  const [blockedByLocation, setBlockedByLocation] = useState(false);
  const sightingService = new SightingService();
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [location, setLocation] = useState(null);
  const [timeEnabled, setTimeEnabled] = useState(true);

  useEffect(() => {
    const now = new Date();
    setDate(toDateInputValue(now));
    setTime(toTimeInputValue(now));
  }, []);

  useEffect(() => {
    if (timeEnabled) {
      const now = new Date();
      setTime(toTimeInputValue(now));
    }
    else {
      setTime('');
    }
  }, [timeEnabled]);

  const toDateInputValue = date => {
    var local = new Date(date);
    local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
  };

  const toTimeInputValue = date => {
    var local = new Date(date);
    local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return local.toJSON().slice(11, 16);
  };
  const handleFormSubmit = async (event) => {
    event.preventDefault();
    if (!blockedByLocation) {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await sightingService.postSighting(accessToken, account.birder.id, bird.binomialName, date, time, location);
        if (response.status === 201) {
          const sightingLocation = response.headers.get('Location');
          const sighting = await sightingService.fetchSightingByLocation(accessToken, sightingLocation);
          onSuccess(sighting);
        }
      }
    }
  };

  return (
    <div className='add-sighting-section'>
      <PageHeading>{t('new-sighting-title')}</PageHeading>
      <div style={{height: '150px', width: '150px', marginLeft: 'auto', marginRight: 'auto'}}>
        <CircledBirdPicture bird={bird} />
      </div>
      <form onSubmit={handleFormSubmit}>
        <BirdSection bird={bird} />
        <div className='date-group'>
          <Label htmlFor='dateInput' label='date-label' />
          <input
            type='date'
            id='dateInput'
            className='date-input'
            value={date}
            onChange={event => setDate(event.target.value)} />
        </div>
        <div className='time-group'>
          <Label htmlFor='timeInput' label='time-label' />
          <div className='time-checkbox-container'>
            <input
              type='checkbox'
              id='timeCheckboxInput'
              name='timeCheckboxInput'
              className='time-checkbox'
              checked={timeEnabled}
              onChange={event => setTimeEnabled(event.target.checked)} />
          </div>
          <input
            type='time'
            id='timeTimeInput'
            className='time-input'
            value={time}
            disabled={!timeEnabled}
            onChange={event => setTime(event.target.value)} />
        </div>
        <LocationSection
          onCoordinatesChanged={setLocation}
          onBlocking={setBlockedByLocation} />
        <button type='submit' disabled={blockedByLocation}>
          {t('submit-sighting-button')}
        </button>
      </form>
      <Link to='/'>{t('cancel-new-sighting-link')}</Link>
    </div>
  );
};
