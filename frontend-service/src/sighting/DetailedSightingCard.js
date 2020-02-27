import React, { useState, useEffect } from 'react';
import { BirdCardName } from '../bird/BirdCardName';
import { useBird } from '../bird/BirdHooks';
import placeholder from '../bird/placeholder-bird.jpg';
import './DetailedSightingCard.scss';

export function DetailedSightingCard({ sighting }) {
  return (
    <div className='detailed-sighting-card card'>
      <CardHeader sighting={sighting} />
      <CardBody sighting={sighting} />
    </div>
  );
}

function CardHeader({ sighting }) {
  const { bird } = useBird(sighting.birdId);
  const [style, setStyle] = useState({});

  useEffect(() => {
    if (bird && bird.cover) {
      setStyle({ backgroundImage: `url(${bird.cover.url})` });
    }
  }, [bird]);

  if (!bird) {
    return null;
  }

  const src = (bird && bird.thumbnail && bird.thumbnail.url) || placeholder;
  return (
    <div className='card-header'>
      <div className='background' style={style} />
      <div className='middle-front'>
        <img src={src} alt="Card" />;
      </div>
    </div>
  );
}

function CardBody({ sighting }) {
  const { bird } = useBird(sighting.birdId);

  if (!bird) {
    return null;
  }

  return (
    <div className='card-body'>
      <BirdCardName bird={bird} />
      <div>{sighting.date}</div>
      <div>{sighting.time}</div>
      {sighting.position && sighting.position.name && <div>{sighting.position.name}</div>}
    </div>
  );
}
