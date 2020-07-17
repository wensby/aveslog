import React from 'react';
import { useBirdStatistics } from './BirdHooks';
import { BirdCover } from './BirdCover.js';
import { CommonNamesSection } from './CommonNamesSection';
import { BirdActionBar } from './BirdActionBar';
import { useTranslation } from 'react-i18next';
import './DetailedBirdCard.scss';

export const DetailedBirdCard = ({ bird }) => {
  const stats = useBirdStatistics(bird);
  const { t } = useTranslation();

  return (
    <div className='detailed-bird-card'>
      <BirdCover bird={bird} />
      <BirdActionBar bird={bird} />
      <CommonNamesSection bird={bird} />
      <hr />
      <div>
        {t('bird-sightings-count-label')}: {stats.sightingsCount}
        <br />
        {t('birders-count-label')}: {stats.birdersCount}
      </div>
      {bird.thumbnail &&
        <div>
          <p><small>{`${t('thumbnail-credit-label')}: ${bird.thumbnail.credit}`}</small></p>
        </div>}
    </div>
  );
};
