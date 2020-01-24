import React, { useState, useEffect } from 'react';
import { useTranslation } from "react-i18next";
import { usePosition } from '../usePosition';
import { ToggleButtonGroup } from '../toggle/ToggleButtonGroup';
import { ToggleButton } from "../toggle/ToggleButton";
import { CoordinatesLoadedIcon } from "./CoordinatesLoadedIcon";
import { CoordinatesLoading } from "./CoordinatesLoading";
import { If } from "./If";

export function LocationSection({ onCoordinatesChanged, onBlocking }) {
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
  }, [selected, coordintes, error]);

  useEffect(() => {
    onBlocking(loading);
  }, [loading, onBlocking]);

  useEffect(() => {
    if (selected === 'current') {
      if (latitude && longitude) {
        setCoordinates([latitude, longitude]);
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
  }, [coordintes, onCoordinatesChanged]);

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
  }, [selected, collapseState]);

  return (
    <div className={`location-section ${collapseState}`}>
      <ToggleButtonGroup onSelected={setSelected}>
        <ToggleButton key='current' value='current'>{t('current-location-label')}</ToggleButton>
        <ToggleButton key='custom' value='custom' disabled={true}>{t('custom-location-label')}</ToggleButton>
      </ToggleButtonGroup>
      <div className='location-expansion'>
        <If condition={selected === 'current'}>
          <CoordinatesLoading display={loading} />
          <CoordinatesLoadedIcon display={coordintes != null} />
        </If>
      </div>
    </div>
  );
}
