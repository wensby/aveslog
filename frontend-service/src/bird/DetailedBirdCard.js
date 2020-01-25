import React from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';
import { useAuthentication } from '../authentication/AuthenticationHooks';
import { CommonNamesSection } from './CommonNamesSection';

export function DetailedBirdCard({ bird }) {
  const { t } = useTranslation();
  const { account } = useAuthentication();
  const stats = useBirdStatistics(bird);

  return (
    <div>
      <BirdCover bird={bird} />
      <CommonNamesSection namesByLanguageCode={bird.names}/>
      <hr />
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
