import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useBird } from './BirdHooks';
import { BirdCover } from './BirdCover.js';

export default function BirdDetails(props) {
  const { t } = useTranslation();
  const { authenticated } = useContext(UserContext);
  const bird = useBird(props.match.params.binomialName);

  const renderPhotoCredits = () => {
    if (bird.thumbnail) {
      return (
        <div>
          <p><small>{`Thumbnail Photo by: ${ bird.thumbnail.credit }`}</small></p>
        </div>
      );
    }
  }

  const renderAddSighting = () => {
    if (authenticated) {
      return <NewBirdSightingLink bird={bird}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
  }

  if (bird) {
    return (
      <div>
        <BirdCover bird={bird} />
        {renderPhotoCredits()}
        {renderAddSighting()}
      </div>
    );
  }
  else {
    return null;
  }
}
