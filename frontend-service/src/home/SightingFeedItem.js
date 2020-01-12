import React from 'react';
import { Link } from 'react-router-dom';
import BirdCardPicture from '../bird/BirdCardPicture';
import BirdLink from '../bird/BirdLink';
import { useTranslation, Trans } from 'react-i18next';
import SightingTime from '../sighting/SightingTime';

export function SightingFeedItem({ birder, sighting, bird }) {
  const { i18n } = useTranslation();
  const name = birder.name;
  const language = i18n.languages[0];
  const birdName = bird.names && bird.names[language] ? bird.names[language] : bird.binomialName;
  return (<div className='sighting-feed-card'>
    <BirdLink bird={bird}>
      <BirdCardPicture bird={bird} />
    </BirdLink>
    <div className='card-body' style={{ padding: '10px' }}>
      <h4>
        {birdName}
      </h4>
      <div>
        <Trans i18nKey='logged-by'>
          Logged by <Link to={`/birder/${birder.id}`}>{{ name }}</Link>
        </Trans>
        <SightingTime sighting={sighting} />
      </div>
    </div>
  </div>);
}
