import React from 'react';
import { useTitle } from 'specific/TitleContext'
import { BirdCover } from './BirdCover.js';
import { CommonNamesSection } from './CommonNamesSection';
import { BirdActionBar } from './BirdActionBar';
import { useTranslation } from 'react-i18next';
import './BirdPage.scss';

export const BirdPage = ({ data }) => {
  const { t, i18n } = useTranslation();
  const language = i18n.languages[0];
  const commonName = data.commonNames.find(commonName => commonName.locale === language).name;
  useTitle(commonName);

  return (
    <div className='detailed-bird-card'>
      <BirdCover bird={data.bird} commonNames={data.commonNames} />
      <BirdActionBar bird={data.bird} />
      <CommonNamesSection bird={data.bird} commonNames={data.commonNames} />
      <hr />
      <div>
        {t('bird-sightings-count-label')}: {data.statistics.sightingsCount}
        <br />
        {t('birders-count-label')}: {data.statistics.birdersCount}
      </div>
      {data.bird.thumbnail &&
        <div>
          <p><small>{`${t('thumbnail-credit-label')}: ${data.bird.thumbnail.credit}`}</small></p>
        </div>}
    </div>
  );
};
