import React from 'react';
import { Link } from 'react-router-dom';
import BirdCardPicture from '../bird/BirdCardPicture';
import BirdLink from '../bird/BirdLink';
import { Trans } from 'react-i18next';
import SightingTime from '../sighting/SightingTime';
import { useBirdName } from '../bird/BirdHooks';

export function SightingFeedItem({ birder, sighting, bird }) {
  const name = birder.name;
  const { local, binomial } = useBirdName(bird);
  return (<div className='sighting-feed-card'>
    <BirdLink bird={bird}>
      <BirdCardPicture bird={bird} />
    </BirdLink>
    <div className='card-body' style={{ padding: '10px' }}>
      <h4>
        {local || binomial}
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
