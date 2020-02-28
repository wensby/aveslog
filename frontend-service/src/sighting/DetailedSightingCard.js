import React, { useState, useEffect } from 'react';
import { BirdCardName } from '../bird/BirdCardName';
import { useBird } from '../bird/BirdHooks';
import { BirdCardPicture } from '../bird/BirdCardPicture';
import './DetailedSightingCard.scss';

export const DetailedSightingCard = ({ sighting }) => {
  return (
    <div className='detailed-sighting-card card'>
      <CardHeader sighting={sighting} />
      <CardBody sighting={sighting} />
    </div>
  );
};

const CardHeader = ({ sighting }) => {
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

  return (
    <div className='card-header'>
      <div className='background' style={style} />
      <div className='middle-front'>
        <BirdCardPicture bird={bird} />
      </div>
    </div>
  );
};

const CardBody = ({ sighting }) => {
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
};
