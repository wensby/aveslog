import React, { useContext, forwardRef, memo } from 'react';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { BirdCardName } from './BirdCardName';
import Icon from '../Icon.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { CircledBirdPicture } from './CircledBirdPicture.js';
import './BirdSearchResultCard.scss';

export const BirdSearchResultCard = memo(forwardRef(({ bird }, ref) => {
  const { authenticated } = useContext(AuthenticationContext);

  if (!bird) {
    return <div className='bird-search-result-card' ref={ref} />;
  }

  return (
    <div className='bird-search-result-card' ref={ref}>
      <CircledBirdPicture bird={bird} />
      <div className='body'>
        <div className='name'>
          <BirdCardName bird={bird} />
          {bird.binomialName}
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
