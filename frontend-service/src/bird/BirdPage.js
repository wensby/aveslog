import React from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { useBird, useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';
import { useAuthentication } from '../authentication/AuthenticationHooks';

export function BirdPage(props) {
  const { t } = useTranslation();
  const { account } = useAuthentication()
  const bird = useBird(props.match.params.binomialName);
  const stats = useBirdStatistics(bird);

  const renderPhotoCredits = () => {
    if (bird.thumbnail) {
      return (
        <div>
          <p><small>{`Thumbnail Photo by: ${bird.thumbnail.credit}`}</small></p>
        </div>
      );
    }
  }

  const renderAddSighting = () => {
    if (account) {
      return <NewBirdSightingLink bird={bird}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
  }

  const renderStats = () => {
    return <div>
      Sightings: {stats.sightingsCount}
      <br/>
      Lucky birders: {stats.birdersCount}
    </div>;
  }

  if (bird) {
    return (
      <div>
        <BirdCover bird={bird} />
        {renderStats()}
        {renderPhotoCredits()}
        {renderAddSighting()}
      </div>
    );
  }
  else {
    return null;
  }
}
