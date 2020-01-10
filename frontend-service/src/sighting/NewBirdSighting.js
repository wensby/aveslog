import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import BirdService from '../bird/BirdService';
import SightingService from './SightingService';
import { UserContext } from '../authentication/UserContext';
import SightingSuccess from './SightingSuccess';
import { usePosition } from '../usePosition';
import Spinner from '../loading/Spinner';
import { ToggleButtonGroup } from '../toggle/ToggleButtonGroup';
import { ToggleButton } from "../toggle/ToggleButton";
import './style.scss';

export default ({ match }) => {
  const binomialName = match.params.binomialName;
  const [addedSighting, setAddedSighting] = useState(null);
  const [bird, setBird] = useState(null);
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [timeEnabled, setTimeEnabled] = useState(true);
  const sightingService = new SightingService();
  const { getAccessToken, account } = useContext(UserContext);
  const { t } = useTranslation();
  const [location, setLocation] = useState(null);
  const [blockedByLocation, setBlockedByLocation] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const data = await new BirdService().getBird(binomialName);
      setBird(data);
    }
    fetchData();
    const now = new Date();
    setDate(toDateInputValue(now));
    setTime(toTimeInputValue(now));
  }, [binomialName]);

  useEffect(() => {
    if (timeEnabled) {
      const now = new Date();
      setTime(toTimeInputValue(now));
    }
    else {
      setTime('');
    }
  }, [timeEnabled]);

  const handleFormSubmit = async event => {
    event.preventDefault();
    if (!blockedByLocation) {
      const accessToken = await getAccessToken();
      const response = await sightingService.postSighting(
        accessToken, account.birder.id, bird.binomialName, date, time, location,
      );
      if (response.status === 201) {
        const sightingLocation = response.headers.get('Location');
        const sighting = await sightingService.fetchSightingByLocation(accessToken, sightingLocation);
        setAddedSighting(sighting);
      }
    }
  }

  const toDateInputValue = date => {
    var local = new Date(date);
    local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
  }

  const toTimeInputValue = date => {
    var local = new Date(date);
    local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return local.toJSON().slice(11, 16);
  }

  if (!bird) {
    return null;
  }

  if (addedSighting) {
    return <SightingSuccess sighting={addedSighting}/>;
  }



  return (
    <div className='container sighting-form'>
      <div className='row'>
        <div className='col'>
          <h1>{t('new-sighting-title')}</h1>
          <form onSubmit={handleFormSubmit}>
            <BirdSection bird={bird} />
            <div className='form-group row'>
              <Label htmlFor='dateInput' label='date-label' />
              <div className='col-sm-10'>
                <input type='date' id='dateInput' className='form-control'
                  value={date}
                  onChange={event => setDate(event.target.value)} />
              </div>
            </div>
            <div className='form-group row'>
              <Label htmlFor='timeInput' label='time-label' />
              <div className='input-group col-sm-10' id='timeInput'>
                <div className='input-group-prepend'>
                  <div className='input-group-text'>
                    <input type='checkbox' id='timeCheckboxInput'
                      name='timeCheckboxInput' checked={timeEnabled}
                      onChange={event => setTimeEnabled(event.target.checked)} />
                  </div>
                </div>
                <input type='time' id='timeTimeInput' className='form-control'
                  value={time} disabled={!timeEnabled}
                  onChange={event => setTime(event.target.value)} />
              </div>
            </div>
            <LocationSection onCoordinatesChanged={setLocation} onBlocking={setBlockedByLocation}/>
            <input type='hidden' name='birdId' value={bird.id} />
            <button type='submit' className='button' disabled={blockedByLocation}>
              {t('submit-sighting-button')}
            </button>
          </form>
          <Link to='/'>{t('cancel-new-sighting-link')}</Link>
        </div>
      </div>
    </div>
  );
}

const BirdSection = ({ bird }) => {
  const { i18n } = useTranslation();
  const language = i18n.languages[0];
  const name = bird.names && bird.names[language] ? bird.names[language] : bird.binomialName;

  return (
    <div className='form-group row'>
      <Label htmlFor='birdInput' label='bird-label' />
      <div className='col-sm-10'>
        <input id='birdInput' type='text' readOnly
          className='col-sm-10 form-control-plaintext'
          value={name} />
      </div>
    </div>
  );
};

const Label = ({ htmlFor, label }) => {
  const { t } = useTranslation();
  const className = 'col-sm-2 col-form-label';
  return <label htmlFor={htmlFor} className={className}>{t(label)}</label>;
};

const LocationSection = ({ onCoordinatesChanged, onBlocking }) => {
  const [coordintes, setCoordinates] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);
  const { latitude, longitude, error } = usePosition(selected === 'current');
  const { t } = useTranslation();
  const [collapseState, setCollapseState] = useState('collapsed');

  useEffect(() => {
    const noCoordinates = coordintes == null;
    const noError = error !== '';
    setLoading(selected === 'current' && noCoordinates && noError);
  }, [selected, coordintes, error])

  useEffect(() => {
    onBlocking(loading);
  }, [loading])

  useEffect(() => {
    if (selected === 'current') {
      if (latitude && longitude) {
        setCoordinates([latitude, longitude])
      }
      else if (error) {
        if (error.toUpperCase() === 'user denied geolocation'.toUpperCase()) {
          setSelected(null);
        }
      }
    }
    else {
      setCoordinates(null);
    }
  }, [selected, latitude, longitude, error]);

  useEffect(() => {
    onCoordinatesChanged(coordintes);
  }, [coordintes]);

  useEffect(() => {
    if (selected !== null && (collapseState === 'collapsed' || collapseState === 'collapsing2')) {
      setCollapseState('expanding');
      setTimeout(() => {
        setCollapseState('expanded');
      }, 300);
    }
    else if (selected === null && (collapseState === 'expanding' || collapseState === 'expanded')) {
      setCollapseState('collapsing2');
      setTimeout(() => {
        setCollapseState('collapsed');
      }, 300);
    }
  }, [selected, collapseState])

  return (
    <div className={`location-section ${collapseState}`}>
      <ToggleButtonGroup onSelected={setSelected}>
        <ToggleButton value='current'>{t('current-location-label')}</ToggleButton>
        <ToggleButton value='custom' disabled={true}>{t('custom-location-label')}</ToggleButton>
      </ToggleButtonGroup>
      <div className='location-expansion'>
        <If condition={selected === 'current'}>
          <CoordinatesLoading display={loading}/>
          <CoordinatesLoadedIcon display={coordintes != null}/>
        </If>
      </div>
    </div>
  );
}

const If = ({condition, children}) => {
  if (condition) {
    return children;
  }
  return null;
}

const CoordinatesLoading = ({display}) => {
  if (display) {
    return <Spinner/>
  }
  return null;
}

const CoordinatesLoadedIcon = ({display}) => {
  if (display) {
    return <div className='loaded-icon'>✓</div>;
  }
  return null;
}
