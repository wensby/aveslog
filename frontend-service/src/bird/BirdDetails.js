import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useBird, useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';

export default function BirdDetails(props) {
  const { t } = useTranslation();
  const { authenticated } = useContext(UserContext);
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
    if (authenticated) {
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
