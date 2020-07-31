import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import SightingService from './SightingService';
import { UserContext } from '../authentication/UserContext';
import { BirdSection } from "./BirdSection";
import { Label } from "./Label";
import { LocationSection } from "./LocationSection";
import { PageHeading } from 'generic/PageHeading';
import { Spinner } from 'generic/Spinner';
import './LogBirdSection.scss';
import { CircledBirdPicture } from 'bird/CircledBirdPicture';

export const LogBirdSection = ({ bird, onSuccess }) => {
  const { t } = useTranslation();
  const { account } = useContext(UserContext);
  const [blockedByLocation, setBlockedByLocation] = useState(false);
  const sightingService = new SightingService();
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [location, setLocation] = useState(null);
  const [timeEnabled, setTimeEnabled] = useState(true);
  const [loading, setLoading] = useState(false);

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
      setLoading(true);
      const response = await sightingService.postSighting(account.birder.id, bird.binomialName, date, time, location);
      if (response.status === 201) {
        const sightingLocation = response.headers['location'];
        const sighting = await sightingService.fetchSightingByLocation(sightingLocation);
        onSuccess(sighting);
      }
      setLoading(false);
    }
  };

  return (
    <div className='log-bird-section'>
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
        <div className='submit-button-group'>
          <button type='submit' disabled={loading || blockedByLocation}>
            {t('submit-sighting-button')}
          </button>
          {loading && <div style={{width: '16px'}}><Spinner/></div>}
        </div>
      </form>
      <Link to='/home'>{t('cancel-new-sighting-link')}</Link>
    </div>
  );
};
