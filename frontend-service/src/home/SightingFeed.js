import React from 'react';
import { Link } from 'react-router-dom';
import { useBird } from '../bird/BirdHooks';
import { useBirder } from '../birder/BirderHooks';
import BirdCardPicture from '../bird/BirdCardPicture';
import BirdLink from '../bird/BirdLink';
import { useTranslation, Trans } from 'react-i18next';
import SightingTime from '../sighting/SightingTime';

export default function SightingFeed({ sightings }) {
  return <>{sightings.map(sighting => <SightingFeedItemContainer sighting={sighting}/>)}</>;
}

function SightingFeedItemContainer({ sighting }) {
  const bird = useBird(sighting.birdId);
  const birder = useBirder(sighting.birderId);
  if (!bird || !birder) {
    return null;
  }
  return <SightingFeedItem sighting={sighting} bird={bird} birder={birder} />;
}

function SightingFeedItem({ birder, sighting, bird }) {
  const { t, i18n } = useTranslation();
  const name = birder.name;
  return (
    <div className='sighting-feed-card'>
      <BirdLink bird={bird} >
        <BirdCardPicture bird={bird} />
      </BirdLink>
      <div className='card-body' style={{padding: '10px'}}>
        <h4>
          {bird.names[i18n.languages[0]] || bird.binomialName}
        </h4>
        <div>
          <Trans i18nKey='logged-by'>
            Logged by <Link to={`/birder/${birder.id}`}>{{name}}</Link>
          </Trans>
          <SightingTime sighting={sighting} />
        </div>
      </div>
    </div>
  );
}
