import React, { useState, useEffect } from 'react';
import { useBird, useCommonName } from '../bird/BirdHooks';
import { BirdThumbnailImage } from '../bird/BirdThumbnailImage';
import './DetailedSightingCard.scss';
import { BirdLink } from 'bird/BirdLink';

export const DetailedSightingCard = ({ sighting }) => {
  const { bird } = useBird(sighting.birdId);
  const { commonName } = useCommonName(bird);
  return (
    <div className='sighting-card'>
      <BackgroundImage bird={bird} />
      <Picture sighting={sighting} />
      <Name name={commonName} />
      <Body>
        {sighting.position && sighting.position.name && <div>{sighting.position.name}</div>}
      </Body>
      <Moment date={sighting.date} time={sighting.time} />
    </div>
  );
};

const Moment = ({date, time}) => {
return <div className='date'>{time ? `${date} - ${time}` : date}</div>
}

const BackgroundImage = ({ bird }) => {
  const [style, setStyle] = useState({});

  useEffect(() => {
    if (bird && bird.cover) {
      setStyle({ backgroundImage: `url(${bird.cover.url})` });
    }
  }, [bird]);

  return (
    <>
      <div className='background picture' style={style} />
      <div className='background body-background' style={style} />
      <div className='background gradient' />
    </>
  );
};

const Body = ({ children }) => {
  return <div class='body'>{children}</div>;
}

const Name = ({ name }) => {
  return <div class='name'>{name}</div>;
};

const Picture = ({ sighting }) => {
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
    <div className='picture'>
      <div className='middle-front'>
        <BirdThumbnailImage bird={bird} />
      </div>
    </div>
  );
};
