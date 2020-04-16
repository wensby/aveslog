import React, { useContext, forwardRef, memo } from 'react';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { BirdCardName } from './BirdCardName';
import Icon from '../Icon.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { PictureBirdLink } from './PictureBirdLink';
import { SightedIndicator } from './SightedIndicator';
import './BirdSearchResultCard.scss';

export const BirdSearchResultCard = memo(forwardRef(({ bird, stats }, ref) => {
  const { authenticated } = useContext(AuthenticationContext);

  if (!bird) {
    return <div className='bird-search-result-card' ref={ref} />;
  }

  return (
    <div className='bird-search-result-card' ref={ref}>
      <PictureBirdLink bird={bird} />
      <div className='body'>
        <div className='name'>
          <BirdCardName bird={bird} />
          {bird.binomialName}
          {authenticated && stats && stats.lastSighting && <SightedIndicator date={stats.lastSighting} />}
        </div>
        {authenticated && <NewSightingButton bird={bird} />}
      </div>
    </div>
  );
}));

const NewSightingButton = ({ bird }) => {
  return (
    <NewBirdSightingLink bird={bird}>
      <Icon name='add'></Icon>
    </NewBirdSightingLink>
  );
}
