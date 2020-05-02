import React, { useContext, useState, useEffect } from 'react';
import { SearchContext } from '../../search/SearchContext.js';
import { useTranslation } from 'react-i18next';
import { Spinner } from 'generic/Spinner';
import './SightedNearbyFormGroup.scss';

const radiusToRangeValue = radius => {
  const minp = 0;
  const maxp = 100;
  const minv = Math.log(1);
  const maxv = Math.log(1000);
  const scale = (maxv-minv) / (maxp-minp);
  return ((Math.log(radius) - minv) / scale) + minp;
};

const sliderValue = position => {
  const minp = 0;
  const maxp = 100;
  const minv = Math.log(1);
  const maxv = Math.log(1000);
  const scale = (maxv-minv) / (maxp-minp);
  return Math.exp(minv + scale*(position-minp));
}

export const SightedNearbyFormGroup = () => {
  const { positionActive, positionRadius, setPositionRadius } = useContext(SearchContext);
  const [rangeValue, setRangeValue] = useState(radiusToRangeValue(positionRadius));

  const handleChange = e => {
    setRangeValue(e.target.value);
  };

  useEffect(() => {
    setPositionRadius(Math.round(sliderValue(rangeValue)));
  }, [rangeValue]);

  const repr = () => {
    return `${positionRadius}km`;
  }

  return (
    <div className='sighted-nearby-group'>
      <Toggle />
      {positionActive &&
        <div>
          {repr()}
          <input type='range' value={rangeValue} min='0' max='100' step='2' onChange={handleChange} style={{ width: '100%' }} />
        </div>
      }
    </div>
  );
};

const Toggle = () => {
  const { positionActive, setPositionActive, position } = useContext(SearchContext);
  const loading = positionActive && !position;
  const { t } = useTranslation();

  const handleChange = e => {
    setPositionActive(e.target.checked);
  }

  const classNames = ['toggle'];
  if (loading) {
    classNames.push('loading');
  }

  return (
    <div className={classNames.join(' ')}>
      {loading && <div><Spinner onClick={() => setPositionActive(false)} /></div>}
      <input id='positionCheckbox' type='checkbox' checked={positionActive} onChange={handleChange} />
      <label htmlFor='positionCheckbox'>{t('search-sighted-nearby-label')}</label>
    </div>
  );
}
