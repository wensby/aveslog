import React from 'react';
import { Link } from 'react-router-dom';
import { Trans } from 'react-i18next';
import { SightingTime } from '../sighting/SightingTime';
import { useCommonName } from '../bird/BirdHooks';
import './SightingFeedItem.scss';
import { PictureBirdLink } from 'bird/PictureBirdLink';

export function SightingFeedItem({ birder, sighting, bird }) {
  const name = birder.name;
  const { commonName, loading } = useCommonName(bird);

  return (
    <div className='feed-card sighting'>
      <PictureBirdLink bird={bird} />
      <div>
        <div className='bird-name'>{loading ? '' : commonName || bird.binomialName}</div>
        <hr />
        <div>
          <Trans i18nKey='logged-by'>
            Logged by <Link to={`/birders/${birder.id}`}>{{ name }}</Link>
          </Trans>
          <div>
          <SightingTime sighting={sighting} />
          </div>
        </div>
      </div>
    </div>
  );
}
