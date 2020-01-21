import React from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { useBird, useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';
import { useAuthentication } from '../authentication/AuthenticationHooks';

export function BirdPage({ match }) {
  const { t } = useTranslation();
  const { account } = useAuthentication()
  const bird = useBird(match.params.binomialName);
  const stats = useBirdStatistics(bird);

  if (bird) {
    return (
      <div>
        <BirdCover bird={bird} />
        <div>
          Sightings: {stats.sightingsCount}
          <br />
          Lucky birders: {stats.birdersCount}
        </div>
        {bird.thumbnail && 
        <div>
          <p><small>{`Thumbnail Photo by: ${bird.thumbnail.credit}`}</small></p>
        </div>}
        {account && <NewBirdSightingLink bird={bird}>{t('add-sighting-link')}</NewBirdSightingLink>}
      </div>
    );
  }
  else {
    return null;
  }
}
