import React, { useContext, forwardRef, memo } from 'react';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { BirdCardName } from './BirdCardName';
import { BirdThumbnailImage } from './BirdThumbnailImage.js';
import { BirdLink } from './BirdLink.js';
import Icon from '../Icon.js';
import './BirdSearchResultCard.scss';

export const BirdSearchResultCard = memo(forwardRef(({ bird }, ref) => {
  const { authenticated } = useContext(UserContext);

  if (!bird) {
    return <div className='bird-search-result-card' ref={ref} />;
  }

  return (
    <div className='bird-search-result-card' ref={ref}>
      <div className='picture'>
        <BirdLink bird={bird} >
          <BirdThumbnailImage bird={bird} />
        </BirdLink>
      </div>
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
  const { t } = useTranslation();
  return (
    <NewBirdSightingLink bird={bird}>
      <Icon name='add'></Icon>
    </NewBirdSightingLink>
  );
}
