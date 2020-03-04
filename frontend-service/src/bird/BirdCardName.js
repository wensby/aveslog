import React from 'react';
import { useCommonName } from './BirdHooks';
import { FadeInBottom } from './FadeInBottom';
import './BirdCardName.scss';

export function BirdCardName({ bird }) {
  const { commonName } = useCommonName(bird);

  if (commonName) {
    return (
      <>
        <FadeInBottom>
          <div className='bird-name'>{commonName}</div>
        </FadeInBottom>
      </>
    )
  }
  return <div className='bird-name'> </div>;
};
