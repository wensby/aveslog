import React from 'react';
import { Link } from 'react-router-dom';
import { useBird } from '../bird/BirdHooks';
import { usePerson } from '../person/PersonHooks';
import BirdCardPicture from '../bird/BirdCardPicture';
import BirdLink from '../bird/BirdLink';
import { useTranslation, Trans } from 'react-i18next';
import SightingTime from '../sighting/SightingTime';

export default function SightingFeed({ sightings }) {
  return <>{sightings.map(sighting => <SightingFeedItemContainer sighting={sighting}/>)}</>;
}

function SightingFeedItemContainer({ sighting }) {
  const bird = useBird(sighting.birdId);
  const person = usePerson(sighting.personId);
  if (!bird || !person) {
    return null;
  }
  return <SightingFeedItem sighting={sighting} bird={bird} birder={person} />;
}

function SightingFeedItem({ birder, sighting, bird }) {
  const { t } = useTranslation();
  const name = birder.name;
  return (
    <div className='sighting-feed-card'>
      <BirdLink bird={bird} >
        <BirdCardPicture bird={bird} />
      </BirdLink>
      <div className='card-body' style={{padding: '10px'}}>
        <h4>
          {t(`bird:${bird.binomialName}`, { fallbackLng: [] })}
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
