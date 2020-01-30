import React from 'react';
import { Link } from 'react-router-dom';
import { BirdCardPicture } from '../bird/BirdCardPicture';
import BirdLink from '../bird/BirdLink';
import { Trans } from 'react-i18next';
import { SightingTime } from '../sighting/SightingTime';
import { useCommonName } from '../bird/BirdHooks';
import './SightingFeedItem.scss';

export function SightingFeedItem({ birder, sighting, bird }) {
  const name = birder.name;
  const { commonName, loading } = useCommonName(bird);

  return (
    <div className='feed-card sighting'>
      <div className='bird-picture'>
        <BirdLink bird={bird} >
          <BirdCardPicture bird={bird} />
        </BirdLink>
      </div>
      <div>
        <div className='bird-name'>{loading ? '' : commonName || bird.binomialName}</div>
        <hr />
        <div>
          <Trans i18nKey='logged-by'>
            Logged by <Link to={`/birder/${birder.id}`}>{{ name }}</Link>
          </Trans>
          <div>
          <SightingTime sighting={sighting} />
          </div>
        </div>
      </div>
    </div>
  );
}
